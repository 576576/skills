<h1 align="center">Skills</h1>

<p align="center">
<a href="../zh/README.md">中文 (简体)</a> &nbsp;|&nbsp; <a href="../zh-Hant/README.md">中文 (繁體)</a> &nbsp;|&nbsp; English
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

## Intro

A collection of reusable agent skills created by 576576.

## Features

 Skill | Purpose
 --- | ---
 ci-matrix | Design and verify a six-workflow GitHub Actions CI
 repo-i18n | Manage multi-language docs via JSON

---

## ci-matrix

**ci-matrix** — Design and verify a multi-workflow GitHub Actions CI: one reusable quality gate (`lint.yml`), one reusable build (`build.yml`), one release entry point (`release.yml`), plus a PR gate, a pre-release cleaner and an i18n updater — six files, each with a single trigger face. Ships the per-file trigger/call matrix and the rules behind it, plus `examples/verify_workflows.py`, which checks YAML, every `run:` block via `bash -n`, `uses:` targets, the `with:` input contract and PR path filters — offline, before pushing.

## repo-i18n

**repo-i18n** — Manage repository multi-language docs: translations live in `assets/docs/*.json`, rendered from `assets/templates/README.md`. `repo-i18n/scripts/render_i18n.py` runs directly from the repo root and rewrites `README.md` + `docs/*/README.md` in place: `--once` is a one-shot clean run (no CI, ignores bundles, no `docs/i18n.md`); `--no-code` is the non-code mode (drops `platforms` before rendering, no platform badge).

## License

MIT © Skills Contributors
