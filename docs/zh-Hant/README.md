<h1 align="center">Skills</h1>

<p align="center">
<a href="../zh/README.md">中文 (简体)</a> &nbsp;|&nbsp; 中文 (繁體) &nbsp;|&nbsp; <a href="../en/README.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

## 簡介

可复用的智能体技能集合，由576576创建。

## 特性

 技能 | 用途
 --- | ---
 ci-matrix | GitHub Actions 六件套 CI 的设计与本地校验
 repo-i18n | 通过 JSON 语言包管理多语言文档

---

## ci-matrix

**ci-matrix** —— 设计与校验一套多 workflow 的 GitHub Actions CI：一个可复用的质量门禁（`lint.yml`）、一个可复用的构建（`build.yml`）、一个唯一发布入口（`release.yml`），外加 PR 把关、预发布清理与 i18n 更新，共六个文件、每个只有一个触发面。含逐文件的触发/调用矩阵与其背后的规则，以及 `examples/verify_workflows.py`：离线检查 YAML、每个 `run:` 块的 `bash -n`、`uses:` 指向的文件、`with:` 输入契约与 PR 上的路径过滤。

## repo-i18n

**repo-i18n** —— 管理仓库多语言文档：翻译存于 `assets/docs/*.json`，由 `assets/templates/README.md` 渲染。`repo-i18n/scripts/render_i18n.py` 可直接在仓库根执行，就地重写 `README.md` 与 `docs/*/README.md`：`--once` 为一次性干净运行（不依赖 CI，忽略 bundles、不写 `docs/i18n.md`）；`--no-code` 为非代码仓库模式（渲染前移除 `platforms`，不生成平台徽章）。

## 許可證

MIT © Skills Contributors
