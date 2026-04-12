# Chinese Tech Doc Style

本项目只是一份面向中文技术文档、产品文案与界面文案的写作 Skill。

这份 Skill 的目标很明确：中文技术写作应更克制、更准确、更易读。不追求宣传感，也不试图把所有内容都写成统一模板，而是聚焦几类高频问题：

- 中文技术文案容易空泛、重复、宣传化
- 中文与英文、数字混合排版时可读性差
- 常见英文状态词和错误词容易被机械直译
- 文档首页、解决方案页、接口说明页、FAQ 的信息密度和结构经常失衡

如果需要一套适合中文技术文档的基础写作规范，这份 Skill 可以直接拿来使用，或是作为参考。

## 适用场景

本 Skill 适合以下内容：

- 文档首页、落地页、首屏文案
- 接口文档、参数说明、错误码说明、更新日志
- 产品能力介绍、解决方案页、能力说明页
- 界面文案、按钮文案、导航标签、提示信息

不适合以下内容：

- 代码字面量
- JSON 键名
- URL
- API 路径
- 数据库字段名
- 其他机器可读标识符

## 核心规则概览

这份 Skill 主要覆盖以下规则：

- 中文引号统一使用直角引号 `「」`
- 不使用 `你`、`您`、`同学` 这类直接称呼
- 在可见正文中处理中文与英文、数字之间的留白
- 避免机械直译 `Success`、`Invalid`、`Bad Request` 等英文状态词
- 避免高频互联网黑话，如 `赋能`、`抓手`、`闭环`、`打通`
- 按钮文案应体现下一步动作，避免与标题重复
- 移动端优先保证可读性，而不是继续沿用桌面排版

完整规范请阅读：

- [NoCode-Skill.md](./NoCode-Skill.md)

## 仓库结构

```text
tech-doc-style-chinese/
├── SKILL.md
├── NoCode-Skill.md
├── README.md
├── agents/
│   └── openai.yaml
└── references/
    └── Project-Overrides.md
```

各文件的作用：

- `SKILL.md`：正式技能入口，供 Codex 使用
- `NoCode-Skill.md`：对外说明稿，适合公开阅读和分享
- `README.md`：GitHub 仓库首页说明
- `agents/openai.yaml`：技能展示元数据
- `references/Project-Overrides.md`：项目私有约定示例

## 如何在 Codex 中使用

如果要把它作为 Skill 安装到本地，可将整个目录放进 `$CODEX_HOME/skills/` 下。

例如：

```bash
mkdir -p "$CODEX_HOME/skills/tech-doc-style-chinese"
cp -R ./* "$CODEX_HOME/skills/tech-doc-style-chinese/"
```

安装完成后，可在任务中显式调用：

```text
Use $tech-doc-style-chinese to rewrite this Chinese technical copy.
```

或者直接在相关任务中触发，例如：

- 重写中文技术文案
- 整理 FAQ
- 优化 API 文档措辞
- 优化落地页中文文案

## 如何做项目级覆盖

这份 Skill 只放通用规则，不把某个项目的版本展示、品牌语气、术语表或信息架构硬编码到核心规范里。

如果项目存在自己的约定，建议通过单独的覆盖文件管理，例如：

- `references/Project-Overrides.md`

这类覆盖文件适合放：

- 版本展示约定
- 品牌或术语偏好
- 文档结构偏好
- 当前项目特有示例

这样可以保持核心 Skill 可复用，同时允许项目自行扩展。

## 发布建议

如果只是公开分享规范内容：

- 保留 `NoCode-Skill.md`
- 用 `README.md` 做仓库首页说明

如果希望别人能直接安装使用：

- 保留 `SKILL.md`
- 保留 `agents/openai.yaml`
- 在仓库里明确目录结构和安装方式

## 作者

- Fenng（GitHub：[@Fenng](https://github.com/Fenng)）

## License

如果准备正式公开发布，有待补一个明确的开源许可证，例如：

- MIT
- Apache-2.0

当前仓库如未附带许可证，默认不等于可自由复用。
