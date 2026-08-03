<p align="center">
  <img src="../../assets/images/icon.png" width="64" alt="Skills">
</p>

<h1 align="center">Skills</h1>

<p align="center">
<a href="../zh/README.md">中文 (简体)</a> &nbsp;|&nbsp; <a href="../zh-Hant/README.md">中文 (繁體)</a> &nbsp;|&nbsp; English
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img alt="version" src="https://img.shields.io/badge/version-0.1.0-informational" />
</p>

<em>A collection of reusable agent skills — starting with repo-i18n for repository internationalization</em>

---

## Features

| Features |
|---|
| Reusable across any repo and agent environment |
| Self-contained skills with references & examples |
| Multi-language docs via JSON bundles (en / zh / zh-Hant) |
| CI-driven README generation from templates |

---

## Build

See [BUILD.md](../docs/BUILD.md) for instructions on adding a new skill.

---

## Architecture

```
Skills/
├── repo-i18n/         The repo-i18n skill (SKILL.md + references/ + examples/)
├── assets/            I18n JSON bundles, docs content, templates
├── .github/workflows/ CI/CD (build.yml)
└── (platform)/
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Content | Markdown · JSON |
| Structure | Skill folders (SKILL.md + references + examples) |
| Generation | Template rendering + CI regeneration |
| I18n | JSON bundles |
| CI/CD | GitHub Actions |

---

## I18n

See [docs/i18n.md](../docs/i18n.md) for language status and contribution guide.

---

## Acknowledgments

| Project | Description |
|---------|-------------|
| Your core framework | VS Code / Claude agent skills |
| Supporting tool / library | GitHub Actions · JSON i18n pipeline |

---

## License

MIT © Skills Contributors
