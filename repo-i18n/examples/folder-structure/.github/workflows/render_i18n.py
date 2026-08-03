#!/usr/bin/env python3
"""Render docs/i18n.md and all READMEs from assets, per the repo-i18n skill.

Inputs (source of truth):
    assets/bundles/*.json        app UI strings per locale
    assets/docs/*.json           README content per locale
    assets/templates/README.md   README template ({{placeholder}} tokens)
    assets/templates/i18n.md     i18n status template
    assets/.i18n_config/i18n.yml root_lang (default en)

Outputs (CI-generated):
    docs/i18n.md                 language coverage table + hash footer
    README.md                    root view of root_lang
    docs/{code}/README.md        docs view for every locale (incl. en)

Driven by env: I18N_DO, DOCS_DO, BUNDLES_HASH, DOCS_HASH, TEMPLATES_HASH, VERSION
"""

import glob
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone

HEADER_KEYS = 4


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def parse_i18n_config():
    """Read assets/.i18n_config/i18n.yml → (root_lang, fallback_map).

    fallback_map is {} when the `fallback` tree is absent or empty.
    """
    try:
        text = read_text("assets/.i18n_config/i18n.yml")
    except FileNotFoundError:
        return "en", {}

    root = "en"
    fallback = {}
    in_fallback = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"root_lang\s*:\s*[\"']?([\w-]+)", line)
        if m:
            root = m.group(1)
            continue
        if line.startswith("fallback:"):
            in_fallback = True
            continue
        if in_fallback:
            if raw[:1] in (" ", "\t") and ":" in line:
                m = re.match(r"([\w-]+)\s*:\s*\[(.*)\]", line)
                if m:
                    code = m.group(1)
                    chain = [x.strip().strip("\"'") for x in m.group(2).split(",") if x.strip()]
                    fallback[code] = chain
                    continue
            # non-indented line → a new top-level key; stop parsing the tree
            break
    return root, fallback


def root_lang():
    root, _ = parse_i18n_config()
    return root


def content_keys(bundle):
    return [k for k in bundle if not k.startswith("_")]


def default_chain(code):
    """Default fallback chain: variant → base → en ; non-variant → en."""
    if "-" in code:
        base = code.split("-", 1)[0]
        chain = [base]
        if base != "en":
            chain.append("en")
        return chain
    return [] if code == "en" else ["en"]


def fallback_chain(code, fallback_map, bundles_by_code, seen=None):
    """Fully expanded, de-duplicated fallback chain for a locale.

    Recursive: after a locale's own chain is exhausted, each hop contributes
    its own (configured or default) chain — e.g. `zh-Hant: [zh]` with
    `zh: [en]` resolves to `[zh, en]`. Cycles are broken and every locale is
    visited at most once.
    """
    if seen is None:
        seen = set()
    seen.add(code)

    if fallback_map:
        configured = fallback_map.get(code)
        direct = configured if configured is not None else default_chain(code)
    else:
        direct = default_chain(code)

    chain = []
    for hop in direct:
        if hop == code or hop in seen:
            continue
        chain.append(hop)
        chain.extend(fallback_chain(hop, fallback_map, bundles_by_code, seen))
    return chain


def effective_keys(code, bundles_by_code, fallback_map):
    """Non-header keys of a locale, merged with every key on its fallback chain."""
    keys = set(content_keys(bundles_by_code[code]))
    for fc in fallback_chain(code, fallback_map, bundles_by_code):
        b = bundles_by_code.get(fc)
        if b:
            keys |= set(content_keys(b))
    return keys


def bundles_sorted():
    """Reverse-alphabetical locale order (sort -r): zh-Hant, zh, ..., en."""
    bundles = []
    for path in sorted(glob.glob("assets/bundles/*.json"), reverse=True):
        bundles.append(load_json(path))
    return bundles


def lang_counts(bundles):
    counts = {}
    for b in bundles:
        counts[b["lang"]] = counts.get(b["lang"], 0) + 1
    return counts


def shared_label(lang, region, counts):
    """Shared labels (e.g. 中文 in zh + zh-Hant) get a region suffix."""
    return f"{lang} ({region})" if counts.get(lang, 0) > 1 else lang


def render_languages(cur_code, doc_prefix, bundles, counts):
    items = []
    for b in bundles:
        label = shared_label(b["lang"], b["langRegion"], counts)
        if b["langCode"] == cur_code:
            items.append(label)  # current language = plain text
        else:
            items.append(f'<a href="{doc_prefix}{b["langCode"]}/README.md">{label}</a>')
    return " &nbsp;|&nbsp; ".join(items)


def deep_merge(base, override):
    """Recursively merge override into base; override wins."""
    out = dict(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_docs_by_code():
    docs = {}
    for path in glob.glob("assets/docs/*.json"):
        d = load_json(path)
        docs[d["langCode"]] = d
    return docs


def merged_doc(code, docs_by_code, fallback_map, bundles_by_code):
    """Locale doc with missing keys filled from its fallback chain."""
    merged = {}
    chain = fallback_chain(code, fallback_map, bundles_by_code)
    for c in list(reversed(chain)) + [code]:
        d = docs_by_code.get(c)
        if d:
            merged = deep_merge(merged, d)
    return merged


def collect_tokens(obj, prefix=""):
    """Flatten a doc into {dot_path: value}; dicts nest, lists become indexed
    (features.title -> features.title.0, features.title.1, ...)."""
    tokens = {}
    for k, v in obj.items():
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            tokens.update(collect_tokens(v, path))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                tokens[f"{path}.{i}"] = item
        else:
            tokens[path] = v
    return tokens


def render_readme(code, out_path, root_view, bundles, counts, docs_by_code, fallback_map, bundles_by_code):
    doc = merged_doc(code, docs_by_code, fallback_map, bundles_by_code)
    tpl = read_text("assets/templates/README.md")

    doc_prefix = "docs/" if root_view else "../"
    icon_prefix = "" if root_view else "../../"

    tpl = tpl.replace("{{icon_prefix}}", icon_prefix)
    tpl = tpl.replace("{{languages}}", render_languages(doc["langCode"], doc_prefix, bundles, counts))
    tpl = tpl.replace("{{version}}", os.environ.get("VERSION", "0.1.0"))

    # whole-value tokens: platforms (URL-encoded), license (plain text)
    if isinstance(doc.get("platforms"), list):
        tpl = tpl.replace("{{platforms}}", urllib.parse.quote(" | ".join(doc["platforms"]), safe=""))
    if doc.get("license") is not None:
        tpl = tpl.replace("{{license}}", str(doc["license"]))

    # dot-path tokens: headings.block1, features.title.0, archTree.dir1.1 ...
    for token, value in collect_tokens(doc).items():
        if token == "platforms":
            continue  # handled above as a whole
        if not root_view and token in ("building", "i18n"):
            # docs view: body doc links become ../docs/...
            value = value.replace("](docs/", "](../docs/")
        tpl = tpl.replace("{{" + token + "}}", str(value))

    write_text(out_path, tpl)


def render_i18n(hashes):
    bundles = bundles_sorted()
    counts = lang_counts(bundles)
    bundles_by_code = {b["langCode"]: b for b in bundles}
    _, fallback_map = parse_i18n_config()
    tpl = read_text("assets/templates/i18n.md")

    en = bundles_by_code["en"]
    actual = len(content_keys(en)) - HEADER_KEYS
    title = load_json("assets/docs/en.json")["title"]

    rows = []
    for b in bundles:
        code = b["langCode"]
        region = b["langRegion"]
        keys = len(effective_keys(code, bundles_by_code, fallback_map)) - HEADER_KEYS
        pct = min(100, round(keys * 100 / actual)) if actual else 100
        n_docs = len(glob.glob(f"docs/{code}/*.md"))
        label = shared_label(b["lang"], region, counts)
        rows.append(
            f"| [{label}]({code}/README.md) | `{code}` | {region} | "
            f"{keys}/{actual} ({pct}%) | {n_docs} 📄 |"
        )

    tpl = tpl.replace("{{title}}", title)
    tpl = tpl.replace("{{date}}", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
    tpl = tpl.replace("{{rows}}", "\n".join(rows))
    tpl = tpl.replace("{{bundles_hash}}", hashes["bundles"])
    tpl = tpl.replace("{{docs_hash}}", hashes["docs"])
    tpl = tpl.replace("{{templates_hash}}", hashes["templates"])

    write_text("docs/i18n.md", tpl)


def main():
    i18n_do = os.environ.get("I18N_DO") == "true"
    docs_do = os.environ.get("DOCS_DO") == "true"
    if not (i18n_do or docs_do):
        print("Nothing to do (I18N_DO=false, DOCS_DO=false)")
        return

    hashes = {
        "bundles": os.environ.get("BUNDLES_HASH", "abcdef12"),
        "docs": os.environ.get("DOCS_HASH", "34567890"),
        "templates": os.environ.get("TEMPLATES_HASH", "fedcba98"),
    }

    bundles = bundles_sorted()
    counts = lang_counts(bundles)
    bundles_by_code = {b["langCode"]: b for b in bundles}
    _, fallback_map = parse_i18n_config()
    rl = root_lang()

    if i18n_do:
        render_i18n(hashes)
        print("Rendered docs/i18n.md")

    if docs_do:
        docs_by_code = load_docs_by_code()
        # docs view for every locale (en included)
        for code in sorted(docs_by_code):
            render_readme(code, f"docs/{code}/README.md", False, bundles, counts,
                          docs_by_code, fallback_map, bundles_by_code)
        # root view for root_lang
        render_readme(rl, "README.md", True, bundles, counts,
                      docs_by_code, fallback_map, bundles_by_code)
        print("Rendered README.md + docs/*/README.md")


if __name__ == "__main__":
    main()
