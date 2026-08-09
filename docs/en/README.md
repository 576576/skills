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
 repo-i18n | Manage multi-language docs via JSON

---

## repo-i18n

**repo-i18n** — Manage repository multi-language docs: translations live in `assets/docs/*.json`, rendered from `assets/templates/README.md`. `repo-i18n/scripts/render_i18n.py` runs directly from the repo root and rewrites `README.md` + `docs/*/README.md` in place: `--once` is a one-shot clean run (no CI, ignores bundles, no `docs/i18n.md`); `--no-code` is the non-code mode (drops `platforms` before rendering, no platform badge).

## License

MIT © Skills Contributors
