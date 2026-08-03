# AGENTS 指南：维护本仓库的多语言文档

本仓库是**非代码仓库**（无应用 UI），用 [`repo-i18n`](repo-i18n/SKILL.md) skill 的
**clear-run 模式**维护多语言 README：**无 CI、无 bundles、无 `docs/i18n.md`** ——
文档完全由本地脚本一次生成并提交。

## 文件布局

```
assets/
├── .i18n_config/i18n.yml     # root_lang: en（+ 可选 fallback 树）
├── docs/
│   ├── en.json               # 根语言（完整内容）
│   ├── zh.json               # 简体中文（完整翻译）
│   └── zh-Hant.json          # 繁体中文：只写 headings（标题），正文靠回退到 zh
├── images/icon.png           # 可选；存在则脚本在 README 顶部附加图标
└── templates/README.md       # Markdown 模板，含 {{点号路径}} 占位符
```

渲染输出（提交到仓库）：
- `README.md` — 根语言视图
- `docs/{en,zh,zh-Hant}/README.md` — 各语言视图

## README 章节结构（约定）

1. `headings.block1` — 简介（`descriptions.desc1`）
2. `headings.block2` — 特性总览（`features` 表格）
3. **每个 skill 一个使用说明 block** — `headings` 中按 `block3`、`block4`… 编号，
   内容在 `skills` 对象中按 **skill 名（字典序）** 存放
4. `headings.license` — 许可证（`{{license}}`）

> 无 Layout/archTree；不要加回目录树。

## 更新流程

1. 编辑 `assets/docs/en.json`（根语言先行，增删改键用
   `python repo-i18n/scripts/keyops.py add/ren/del ...`，支持 `--after`/`--before`；
   手动编辑仅作最后回退）
2. 同步编辑 `assets/docs/zh.json`
3. `assets/docs/zh-Hant.json` 仅当标题需要繁体时才改，正文靠回退，不要补全所有键
4. 如模板占位符有变，编辑 `assets/templates/README.md`
5. 从仓库根重新渲染（本仓库为非代码仓库，显式加 `--no-code`）：

   ```bash
   python repo-i18n/scripts/clear_run.py --no-code
   ```

   会重写 `README.md` 与 `docs/*/README.md`（忽略 bundles、不写 `docs/i18n.md`）。
6. 检查输出无残留 `{{...}}`，然后提交全部变更。

## 新增一个 skill

1. 在仓库根新建 `<name>/SKILL.md`（及配套文件）
2. 在三个 docs JSON 的 `skills` 对象中**按字典序**加入 `<name>` 键，
   并为其分配下一个 `headings.blockN`（标题用 skill 名）
3. 在模板 `assets/templates/README.md` 中按字典序位置插入对应 `{{skills.<name>}}` 块
4. 运行 clear_run.py 重新渲染

## 注意

- 不要重建 `.github/workflows`（CI 已移除）
- 不要恢复 `assets/bundles/` 或 `docs/i18n.md`（clear-run 不读不写）
- 每个 skill 的 block 与 `skills` 键都按字典序排列
