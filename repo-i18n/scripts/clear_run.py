#!/usr/bin/env python3
"""clear_run.py — one-shot document refresh, no CI, no `.github` writes.

Run from the repo root:

    python3 scripts/clear_run.py            # clean run (default)
    python3 scripts/clear_run.py --no-code  # non-code repo (no app UI)

- If `assets/docs/*.json` exists: renders the root `README.md` (root_lang)
  and `docs/{code}/README.md` for every locale from
  `assets/templates/README.md`. Missing folders/files are skipped.
- **Bundles are ignored**: no coverage table, no `docs/i18n.md`.
- `--no-code` explicitly declares a **non-code** repo (no app UI): even if
  `assets/bundles/` exists it is ignored, and `docs/i18n.md` is never written
  (the coverage table needs bundles).
- Otherwise: creates a minimal **Chinese** `README.md` only when it is
  missing.
- `.github/` and CI are never read or written.
"""

import argparse
import glob
import json
import os
import re
import sys
import urllib.parse


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def write_text(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except OSError:
        return None


def parse_i18n_config():
    """Read assets/.i18n_config/i18n.yml -> (root_lang, fallback_map)."""
    root = "en"
    fallback = {}
    text = read_text("assets/.i18n_config/i18n.yml")
    if text is None:
        return root, fallback
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
                    fallback[code] = [x.strip().strip("\"'")
                                      for x in m.group(2).split(",") if x.strip()]
                    continue
            break
    return root, fallback


def default_chain(code):
    """Default fallback: variant -> base -> en ; non-variant -> en."""
    if "-" in code:
        base = code.split("-", 1)[0]
        chain = [base]
        if base != "en":
            chain.append("en")
        return chain
    return [] if code == "en" else ["en"]


def fallback_chain(code, fallback_map, seen=None):
    """Fully expanded, de-duplicated fallback chain (recursive)."""
    if seen is None:
        seen = set()
    seen.add(code)
    direct = fallback_map.get(code, default_chain(code)) if fallback_map else default_chain(code)
    chain = []
    for hop in direct:
        if hop == code or hop in seen:
            continue
        chain.append(hop)
        chain.extend(fallback_chain(hop, fallback_map, seen))
    return chain


def deep_merge(base, override):
    out = dict(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def docs_sorted():
    """All locale docs, reverse-alphabetical by file path (sort -r)."""
    docs = []
    for path in sorted(glob.glob("assets/docs/*.json"), reverse=True):
        d = load_json(path)
        if d:
            docs.append(d)
    return docs


def merged_doc(code, docs_by_code, fallback_map):
    """Locale doc with missing keys filled from its fallback chain."""
    merged = {}
    for c in list(reversed(fallback_chain(code, fallback_map))) + [code]:
        d = docs_by_code.get(c)
        if d:
            merged = deep_merge(merged, d)
    return merged


def collect_tokens(obj, prefix=""):
    """Flatten a doc into {dot_path: value}; dicts nest, lists get indexes."""
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


def render_languages(cur_code, doc_prefix, docs):
    counts = {}
    for d in docs:
        lang = d.get("lang", d.get("langCode", ""))
        counts[lang] = counts.get(lang, 0) + 1
    items = []
    for d in docs:
        lang = d.get("lang", d.get("langCode", ""))
        region = d.get("langRegion", "")
        label = f"{lang} ({region})" if counts.get(lang, 0) > 1 else lang
        code = d["langCode"]
        if code == cur_code:
            items.append(label)
        else:
            items.append(f'<a href="{doc_prefix}{code}/README.md">{label}</a>')
    return " &nbsp;|&nbsp; ".join(items)


def render_readme(doc, out_path, root_view, docs, fallback_map, docs_by_code):
    merged = merged_doc(doc["langCode"], docs_by_code, fallback_map)
    tpl = read_text("assets/templates/README.md")
    if tpl is None:
        return False  # missing template -> skip

    doc_prefix = "docs/" if root_view else "../"
    icon_prefix = "" if root_view else "../../"

    out = tpl.replace("{{icon_prefix}}", icon_prefix)
    out = out.replace("{{languages}}",
                      render_languages(doc["langCode"], doc_prefix, docs))

    if isinstance(merged.get("platforms"), list):
        out = out.replace("{{platforms}}",
                          urllib.parse.quote(" | ".join(merged["platforms"]), safe=""))
    if merged.get("license") is not None:
        out = out.replace("{{license}}", str(merged["license"]))

    for token, value in collect_tokens(merged).items():
        if token == "platforms":
            continue
        out = out.replace("{{" + token + "}}", str(value))

    icon_html = ""
    if os.path.exists("assets/images/icon.png"):
        icon_html = (
            '<p align="center">\n'
            f'  <img src="{icon_prefix}assets/images/icon.png" width="64" '
            f'alt="{merged.get("title", "")}">\n'
            '</p>\n\n'
        )
    write_text(out_path, icon_html + out)
    return True


SIMPLE_README = """# {repo}

本仓库已接入 **repo-i18n** 国际化文档系统。

- 配置文件：`assets/.i18n_config/i18n.yml`
- 语言内容：`assets/docs/`（README 内容）与 `assets/bundles/`（UI 字符串）
- 渲染模板：`assets/templates/README.md`

这是 `clear_run.py` 生成的占位 README。添加 `assets/docs/{{code}}.json` 后
再次运行 `python3 repo-i18n/scripts/clear_run.py` 即可生成多语言 README。
"""


def create_simple_readme():
    if os.path.exists("README.md"):
        print("No assets/docs and README.md already exists — skipped.")
        return False
    repo = os.path.basename(os.getcwd()) or "repo"
    write_text("README.md", SIMPLE_README.format(repo=repo))
    print(f"Created simple Chinese README.md ({repo})")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="One-shot doc refresh (clear run): no CI, no .github writes.")
    parser.add_argument(
        "--no-code", action="store_true",
        help="Declare a non-code repo (no app UI): ignore assets/bundles/ even "
             "if present and never write docs/i18n.md (it needs bundles).")
    args = parser.parse_args(argv)

    if args.no_code:
        print("Non-code mode: assets/bundles/ ignored, docs/i18n.md skipped.")

    docs = docs_sorted()
    if not docs:
        return 0 if create_simple_readme() else 0

    rl, fallback_map = parse_i18n_config()
    docs_by_code = {d["langCode"]: d for d in docs}

    root_doc = next((d for d in docs if d["langCode"] == rl), docs[0])
    if render_readme(root_doc, "README.md", True, docs, fallback_map, docs_by_code):
        print(f"Rendered README.md ({root_doc['langCode']})")
    else:
        print("No assets/templates/README.md — root README skipped.")

    n = 0
    for d in docs:
        if render_readme(d, f"docs/{d['langCode']}/README.md", False, docs, fallback_map, docs_by_code):
            n += 1
    print(f"Rendered {n} docs/{{code}}/README.md (bundles ignored, no i18n.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
