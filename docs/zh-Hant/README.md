<p align="center">
  <img src="../../assets/images/icon.png" width="64" alt="Skills">
</p>

<h1 align="center">Skills</h1>

<p align="center">
<a href="../zh/README.md">中文 (简体)</a> &nbsp;|&nbsp; 中文 (繁體) &nbsp;|&nbsp; <a href="../en/README.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img alt="version" src="https://img.shields.io/badge/version-0.1.0-informational" />
</p>

<em>可重用的智能體技能集合——以 repo-i18n（倉庫國際化）為起點</em>

---

## 功能特性

| 功能特性 |
|---|
| 可在任意倉庫和智能體環境中重用 |
| 自帶引用與示例的完整技能 |
| 透過 JSON 語言包實現多語言文檔（en / zh / zh-Hant） |
| 由 CI 基於模板自動生成 README |

---

## 構建

新增技能的說明請參閱 [BUILD.md](../docs/BUILD.md)。

---

## 架構

```
Skills/
├── repo-i18n/         repo-i18n 技能（SKILL.md + references/ + examples/）
├── assets/            I18n JSON 語言包、文檔內容、模板
├── .github/workflows/ CI/CD（build.yml）
└── (platform)/
```

---

## 技術棧

| 層 | 技術 |
|-------|------------|
| 內容 | Markdown · JSON |
| 結構 | 技能目錄（SKILL.md + references + examples） |
| 生成 | 模板渲染 + CI 自動再生 |
| 國際化 | JSON 語言包 |
| CI/CD | GitHub Actions |

---

## 國際化

請參閱 [docs/i18n.md](../docs/i18n.md) 了解各語言狀態和貢獻指南。

---

## 鳴謝

| 項目 | 說明 |
|---------|-------------|
| Your core framework | VS Code / Claude 智能體技能 |
| Supporting tool / library | GitHub Actions · JSON 國際化流水線 |

---

## 許可證

MIT © Skills Contributors
