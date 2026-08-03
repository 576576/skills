#!/usr/bin/env python3
"""keyops.py — keep every locale's JSON key set in sync (repo-i18n).

Run this when adding, renaming, or removing a translation key so all language
files stay consistent — manual model edits are only a final fallback.

Usage:
  python3 keyops.py add   <json> <key> [value]    # add key to every locale
  python3 keyops.py ren   <json> <old> <new>      # rename key in every locale
  python3 keyops.py del   <json> <key>            # remove key from every locale
  python3 keyops.py check [json]                  # report key-set drift vs target

<json> is any locale file (usually en.json). Sibling locale files in the same
folder (e.g. zh.json, zh-Hant.json) are updated together.

- `add`: the target file gets `value` (default ""); every other locale gets ""
  as a to-translate placeholder.
- Keys starting with `_` are comments: `add` only touches the file you name,
  and `check` ignores them.
- After key ops, translate the placeholders, run `check`, then push — CI
  regenerates docs/i18n.md and the READMEs.
"""

import glob
import json
import os
import sys

HELP = __doc__.strip()


def siblings(path):
    """All locale JSON files in the same folder as path."""
    folder = os.path.dirname(path) or "."
    return sorted(glob.glob(os.path.join(folder, "*.json")))


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def is_comment(key):
    return key.startswith("_")


def cmd_add(path, key, value):
    if is_comment(key):
        # comments are per-language notes: only touch the named file
        data = load(path)
        if key in data:
            print(f"skip {path}: {key!r} already exists")
            return 1
        data[key] = value if value else ""
        save(path, data)
        print(f"added comment {key!r} to {path}")
        return 0

    target = os.path.abspath(path)
    changed = False
    for p in siblings(path):
        data = load(p)
        if key in data:
            print(f"skip {p}: {key!r} already exists")
            continue
        data[key] = value if os.path.abspath(p) == target else ""
        save(p, data)
        print(f"added {key!r} -> {p}")
        changed = True
    return 0 if changed else 1


def cmd_del(path, key):
    changed = False
    for p in siblings(path):
        data = load(p)
        if key in data:
            del data[key]
            save(p, data)
            print(f"removed {key!r} from {p}")
            changed = True
        else:
            print(f"skip {p}: no key {key!r}")
    return 0 if changed else 1


def cmd_ren(path, old, new):
    if old == new:
        print("old and new are the same")
        return 1
    changed = False
    for p in siblings(path):
        data = load(p)
        if old not in data:
            print(f"skip {p}: no key {old!r}")
            continue
        renamed = {}
        for k, v in data.items():
            renamed[new if k == old else k] = v
        save(p, renamed)
        print(f"renamed {old!r} -> {new!r} in {p}")
        changed = True
    return 0 if changed else 1


def cmd_check(path):
    base = load(path)
    base_keys = [k for k in base if not is_comment(k)]
    ok = True
    for p in siblings(path):
        data = load(p)
        keys = set(k for k in data if not is_comment(k))
        base_set = set(base_keys)
        missing = sorted(k for k in base_keys if k not in keys)
        extra = sorted(k for k in keys if k not in base_set)
        if missing or extra:
            ok = False
            print(f"{p}: missing={missing} extra={extra}")
        else:
            print(f"{p}: OK ({len(base_keys)} keys)")
    return 0 if ok else 1


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(HELP)
        return 0

    cmd = argv[0]
    if cmd == "add":
        if len(argv) < 3:
            print("usage: keyops.py add <json> <key> [value]")
            return 2
        return cmd_add(argv[1], argv[2], argv[3] if len(argv) > 3 else "")
    if cmd == "del":
        if len(argv) < 3:
            print("usage: keyops.py del <json> <key>")
            return 2
        return cmd_del(argv[1], argv[2])
    if cmd == "ren":
        if len(argv) < 4:
            print("usage: keyops.py ren <json> <old> <new>")
            return 2
        return cmd_ren(argv[1], argv[2], argv[3])
    if cmd == "check":
        return cmd_check(argv[1] if len(argv) > 1 else "assets/bundles/en.json")

    print(f"unknown command: {cmd}\n")
    print(HELP)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
