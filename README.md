<h1 align="center">Skills</h1>

<p align="center">
中文 (简体) &nbsp;|&nbsp; <a href="docs/zh-Hant/README.md">中文 (繁體)</a> &nbsp;|&nbsp; <a href="docs/en/README.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

## 简介

可复用的智能体技能集合，由576576创建。

## 特性

 技能 | 用途
 --- | ---
 repo-i18n | 通过 JSON 语言包管理多语言文档

---

## repo-i18n

**repo-i18n** —— 管理仓库多语言文档：翻译存于 `assets/docs/*.json`，由 `assets/templates/README.md` 渲染。`repo-i18n/scripts/render_i18n.py` 可直接在仓库根执行，就地重写 `README.md` 与 `docs/*/README.md`：`--once` 为一次性干净运行（不依赖 CI，忽略 bundles、不写 `docs/i18n.md`）；`--no-code` 为非代码仓库模式（渲染前移除 `platforms`，不生成平台徽章）。

## 许可证

MIT © Skills Contributors
