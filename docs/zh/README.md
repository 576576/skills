<p align="center">
  <img src="../../assets/images/icon.png" width="64" alt="Skills">
</p>

<h1 align="center">Skills</h1>

<p align="center">
中文 (简体) &nbsp;|&nbsp; <a href="../zh-Hant/README.md">中文 (繁體)</a> &nbsp;|&nbsp; <a href="../en/README.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img alt="version" src="https://img.shields.io/badge/version-0.1.0-informational" />
</p>

<em>可复用的智能体技能集合——以 repo-i18n（仓库国际化）为起点</em>

---

## 特性

| 特性 |
|---|
| 可在任意仓库和智能体环境中复用 |
| 自带引用与示例的完整技能 |
| 通过 JSON 语言包实现多语言文档（en / zh / zh-Hant） |
| 由 CI 基于模板自动生成 README |

---

## 构建

添加新技能的说明请参阅 [BUILD.md](../docs/BUILD.md)。

---

## 架构

```
Skills/
├── repo-i18n/         repo-i18n 技能（SKILL.md + references/ + examples/）
├── assets/            I18n JSON 语言包、文档内容、模板
├── .github/workflows/ CI/CD（build.yml）
└── (platform)/
```

---

## 技术栈

| 层 | 技术 |
|-------|------------|
| 内容 | Markdown · JSON |
| 结构 | 技能目录（SKILL.md + references + examples） |
| 生成 | 模板渲染 + CI 自动再生 |
| 国际化 | JSON 语言包 |
| CI/CD | GitHub Actions |

---

## 国际化

语言状态与贡献指南请参阅 [docs/i18n.md](../docs/i18n.md)。

---

## 致谢

| 项目 | 说明 |
|---------|-------------|
| Your core framework | VS Code / Claude 智能体技能 |
| Supporting tool / library | GitHub Actions · JSON 国际化流水线 |

---

## 许可证

MIT © Skills Contributors
