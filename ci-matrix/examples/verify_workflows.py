#!/usr/bin/env python
"""Verify a GitHub Actions workflow set locally, before pushing.

    python verify_workflows.py [repo_root] [--expect expectations.json]

Why: a workflow's `run:` blocks are shell scripts and its `uses:`/`with:` wiring
is a contract between files. Both fail far from their cause — a `uses:` typo
fails only when that caller is triggered, a missing input only on the run that
needs it, and a 10-minute matrix costs more than the check. Everything here is
local, offline and re-runnable.

Checks
  1. every .github/workflows/*.yml parses and declares jobs
  2. every `run:` block passes `bash -n`  (pwsh steps excepted)
  3. every `uses: ./.github/workflows/x.yml` points at a file that exists
  4. a reusable workflow (workflow_call) does not also follow push / pull_request
  5. a pull_request-triggered file does not use `paths` / `paths-ignore`
     (a skipped workflow is absent: the PR has no check at all)
  6. every required input of a called workflow is passed in `with:`,
     and no `with:` key is unknown to the callee
  7. with --expect: each file's trigger face matches expectations.json

expectations.json shape (optional):
    {"lint.yml": ["workflow_call", "workflow_dispatch"],
     "release.yml": ["push", "workflow_dispatch"]}
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

FAILED: list[str] = []


def ok(cond: bool, label: str, detail: str = "") -> None:
    print(f"{'OK  ' if cond else 'FAIL'} {label}" + (f"  <- {detail}" if detail and not cond else ""))
    if not cond:
        FAILED.append(label)


def on_map(doc: dict) -> dict:
    """`on:` as a mapping. YAML 1.1 parses a bare `on` as the boolean True."""
    on = doc.get("on", doc.get(True))
    return on if isinstance(on, dict) else {}


def triggers(doc: dict) -> set[str]:
    on = doc.get("on", doc.get(True))
    if on is None:
        return set()
    return {on} if isinstance(on, str) else set(on)


def run_blocks(doc: dict):
    """Yield (job, step label, script) for every bash-backed `run:`."""
    for job, body in (doc.get("jobs") or {}).items():
        for step in body.get("steps") or []:
            script = step.get("run")
            if not isinstance(script, str):
                continue
            shell = str(step.get("shell") or "")
            if "pwsh" in shell or "powershell" in shell:
                continue
            yield job, step.get("name") or step.get("id") or "<unnamed>", script


def find_bash() -> str:
    found = shutil.which("bash")
    if found:
        return found
    for candidate in (r"C:\Program Files\Git\bin\bash.exe",
                      "/usr/bin/bash", "/bin/bash"):
        if Path(candidate).exists():
            return candidate
    return "bash"


def declared_inputs(doc: dict) -> dict[str, dict]:
    return ((on_map(doc).get("workflow_call") or {}).get("inputs") or {})


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    root = Path(args[0] if args else ".").resolve()
    expect_path = None
    if "--expect" in argv:
        expect_path = Path(argv[argv.index("--expect") + 1])
    wf_dir = root / ".github" / "workflows"
    if not wf_dir.is_dir():
        print(f"no {wf_dir}")
        return 2

    docs: dict[str, dict] = {}
    for path in sorted(wf_dir.glob("*.yml")):
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            ok(False, f"{path.name} parses", str(exc).replace("\n", " ")[:160])
            continue
        ok(isinstance(doc, dict) and bool(doc.get("jobs")), f"{path.name} parses and has jobs")
        docs[path.name] = doc
    print(f"--- {len(docs)} workflow file(s) under {wf_dir}")

    # 1) syntax of every run block (written to a temp file: some blocks are KB-sized)
    total = bad = 0
    bash = find_bash()
    for name, doc in docs.items():
        for job, step, script in run_blocks(doc):
            total += 1
            with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False,
                                             encoding="utf-8", newline="\n") as fh:
                fh.write(script)
                tmp = Path(fh.name)
            try:
                proc = subprocess.run([bash, "-n", str(tmp).replace("\\", "/")],
                                      capture_output=True, text=True)
            finally:
                tmp.unlink(missing_ok=True)
            if proc.returncode != 0:
                bad += 1
                ok(False, f"{name} / {job} / {step} syntax", (proc.stderr or "").strip()[:200])
    ok(bad == 0, f"{total} run block(s) pass bash -n", f"{bad} failed")

    # 2) structural rules
    for name, doc in docs.items():
        trig = triggers(doc)
        if "workflow_call" in trig:
            extra = trig & {"push", "pull_request", "pull_request_target"}
            ok(not extra, f"{name} is reusable only (no push/PR face)", str(sorted(extra)))
        if "pull_request" in trig or "pull_request_target" in trig:
            pr_on = on_map(doc).get("pull_request") or {}
            ok(not ({"paths", "paths-ignore"} & set(pr_on if isinstance(pr_on, dict) else {})),
               f"{name} has no paths filter on pull_request",
               str(pr_on))

    # 3) `uses:` targets exist, and the with: contract matches
    for name, doc in docs.items():
        for job, body in (doc.get("jobs") or {}).items():
            uses = body.get("uses")
            if not isinstance(uses, str) or not uses.startswith("./"):
                continue
            target = uses.split("@")[0].lstrip("./")
            fname = Path(target).name
            ok(fname in docs, f"{name} / {job}: uses {uses} exists", str(sorted(docs)))
            if fname not in docs:
                continue
            declared = declared_inputs(docs[fname])
            required = {k for k, v in declared.items()
                        if isinstance(v, dict) and v.get("required") and "default" not in v}
            provided = set(body.get("with") or {})
            ok(required <= provided, f"{name} / {job}: all required inputs passed",
               f"missing {sorted(required - provided)}")
            ok(provided <= set(declared), f"{name} / {job}: no unknown inputs",
               f"unknown {sorted(provided - set(declared))}")

    # 4) optional trigger-face expectations
    if expect_path:
        expected = json.loads(expect_path.read_text(encoding="utf-8"))
        for fname, want in expected.items():
            ok(fname in docs, f"{fname} exists")
            if fname in docs:
                ok(triggers(docs[fname]) == set(want), f"{fname} trigger face",
                   f"{sorted(triggers(docs[fname]))} != {sorted(want)}")

    print()
    if FAILED:
        print(f"{len(FAILED)} failed:")
        for f in FAILED:
            print(f"  - {f}")
        return 1
    print(f"all checks passed ({total} run block(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
