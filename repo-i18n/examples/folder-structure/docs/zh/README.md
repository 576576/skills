<p align="center">
  <img src="../../assets/images/icon.png" width="64" alt="FlCroc">
</p>

<h1 align="center">FlCroc</h1>

<p align="center">
<a href="../en/README.md">English</a> &nbsp;|&nbsp; 中文 (简体)
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Android%20%7C%20Windows%20%7C%20Linux-blue" alt="Platform">
  <img src="https://img.shields.io/badge/license-GPL v3-green" alt="License">
  <img alt="version" src="https://img.shields.io/badge/version-1.2.3-informational" />
</p>

<em>基于 croc 的 Flutter GUI——在计算机之间轻松安全地传输文件</em>

---

## ✨ 特性

| | 特性 |
|---|-----|
| 🖥️ | 跨平台（Windows、Linux、Android） |
| 🔒 | 通过 croc 进行端到端加密文件传输 |
| 🌍 | 原生多语言支持 |
| 🌙 | 现代 Flutter UI，自适应布局 |

---

## 🚀 构建

构建说明和各平台指南请参阅 [BUILD.md](../docs/BUILD.md)。

---

## 🏗️ 架构

```
FlCroc/
├── lib/               Flutter 应用（Riverpod + Material 3）
├── go_bridge/         Go CGO 共享库（FFI 桥接）
├── submodules/croc/   vendored croc 源码
├── assets/            应用图标、I18n JSON 语言包
├── .github/workflows/ CI/CD（build.yml）
└── (platform)/
```

---

## 🧰 技术栈

| 层 | 技术 |
|-------|------------|
| UI | Flutter 3.x · Material 3 |
| 状态管理 | Riverpod · Freezed |
| 后端 | Go CGO FFI · croc 子模块 |
| 国际化 | JSON 语言包 |
| CI/CD | GitHub Actions |

---

## 🌍 国际化

语言状态与贡献指南请参阅 [docs/i18n.md](../docs/i18n.md)。

---

## 🙏 致谢

| 项目 | 说明 |
|---------|-------------|
| [croc](https://github.com/schollz/croc) | 后端文件传输引擎 |
| [Flutter](https://flutter.dev) | 跨平台 UI 框架 |
| [FlClash](https://github.com/chen08209/FlClash) | UI 灵感来源 |
| [croc-app](https://github.com/Dking08/croc-app) | 二维码扫描参考 |

---

## 📄 许可证

GPL3 © FlCroc Contributors
