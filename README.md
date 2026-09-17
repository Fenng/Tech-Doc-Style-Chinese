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

- 改写时保留事实、限制、条件和确定程度
- 中文引号统一使用直角引号 `「」`
- 默认避免不必要的直接称呼，允许项目语气覆盖
- 在可见正文中处理中文与英文、数字之间的留白
- 中文段落在源文件中保持一段一行，不做硬换行
- 避免机械直译 `Success`、`Invalid`、`Bad Request` 等英文状态词
- 避免高频互联网黑话，如 `赋能`、`抓手`、`闭环`、`打通`
- 对操作、排查和运维文档应用受控中文技术写作方法

完整规范请阅读：

- [SKILL.md](./SKILL.md)
- [公开说明稿](./NoCode-Skill.md)

## 仓库结构

```text
tech-doc-style-chinese/
├── SKILL.md
├── NoCode-Skill.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── api-status-copy.md
│   ├── controlled-technical-chinese.md
│   ├── project-overrides-example.md
│   └── terminology-and-typography.md
├── scripts/
│   ├── lint_copy_rules.py
│   └── unwrap_md_paragraphs.py
└── tests/
    ├── test_lint_copy_rules.py
    ├── test_skill_structure.py
    └── test_unwrap_md_paragraphs.py
```

各文件的作用：

- `SKILL.md`：正式技能入口，供 Codex、Claude Code 等 Agent 使用
- `NoCode-Skill.md`：对外说明稿，适合公开阅读和分享
- `README.md`：GitHub 仓库首页说明
- `agents/openai.yaml`：技能展示元数据
- `references/`：按任务读取的详细规则和项目覆盖模板
- `scripts/lint_copy_rules.py`：轻量检查器
- `scripts/unwrap_md_paragraphs.py`：展开段落硬换行的工具
- `tests/`：检查器、技能结构和硬换行工具的回归测试

## 如何在 Codex 中使用

### 使用 npx 安装（推荐）

如果本机有 Node.js 环境，可直接用 `npx skills` 安装：

```bash
# 直接安装
npx skills add https://github.com/Fenng/tech-doc-style-chinese
```

如需无交互并明确安装到全局 Codex，可使用：

```bash
npx -y skills add https://github.com/Fenng/tech-doc-style-chinese -a codex -g
```

参数说明：

- `-a codex` 表示安装到 Codex agent
- `-g` 表示全局安装（用户级），不加则安装到当前项目范围
- `-y` 表示跳过交互确认，便于自动化执行

安装后建议重启 Codex，以确保新 Skill 被加载。

### 按 Release 安装（推荐）

固定版本安装，便于团队复现：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"

git clone --depth 1 --branch <release-tag> \
  https://github.com/Fenng/tech-doc-style-chinese.git \
  "$CODEX_HOME/skills/tech-doc-style-chinese"
```

`<release-tag>` 可替换为已发布版本，例如 `v0.1.0.2.4`。

### 本地目录安装（开发场景）

如果正在本地修改或调试，可直接复制目录：

```bash
mkdir -p "$CODEX_HOME/skills/tech-doc-style-chinese"
cp -R ./* "$CODEX_HOME/skills/tech-doc-style-chinese/"
```

安装后可快速校验：

```bash
test -f "$CODEX_HOME/skills/tech-doc-style-chinese/SKILL.md" && echo "installed"
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

## 如何在 Claude Code 中使用

### 直接让 Claude Code 安装（最简单）

如果当前 Claude Code 环境支持安装 Skills，可让它读取本仓库并安装：

```text
请安装这份 Skill：https://github.com/Fenng/tech-doc-style-chinese
```

这种方式较省事，但具体装到项目级还是全局取决于 Claude Code 当时的能力与判断。团队协作或需要写进文档、CI 的场景，建议用下面的 npx 命令。

### 使用 npx 安装（推荐）

如果本机有 Node.js 环境，可直接用 `npx skills` 安装：

```bash
# 安装到当前项目
npx skills add https://github.com/Fenng/tech-doc-style-chinese -a claude-code
```

如需无交互并明确安装到全局 Claude Code，可使用：

```bash
npx -y skills add https://github.com/Fenng/tech-doc-style-chinese -a claude-code -g
```

参数说明：

- `-a claude-code` 表示安装到 Claude Code
- `-g` 表示全局安装（用户级，写入 `~/.claude/skills/`），不加则安装到当前项目范围（写入 `./.claude/skills/`）
- `-y` 表示跳过交互确认，便于自动化执行

安装后建议重启 Claude Code，以确保新 Skill 被加载。

### 本地目录安装（开发场景）

如果正在本地修改或调试，可直接复制目录：

```bash
mkdir -p ~/.claude/skills/tech-doc-style-chinese
cp SKILL.md ~/.claude/skills/tech-doc-style-chinese/
cp -R references ~/.claude/skills/tech-doc-style-chinese/
```

安装后可快速校验：

```bash
test -f ~/.claude/skills/tech-doc-style-chinese/SKILL.md && echo "installed"
```

Claude Code 会根据 `SKILL.md` 里的 `description` 自动判断何时调用该 Skill，无须手动触发，例如：

- 重写中文技术文案
- 整理 FAQ
- 优化 API 文档措辞
- 优化落地页中文文案

## 如何做项目级覆盖

这份 Skill 只放通用规则，不把某个项目的版本展示、品牌语气、术语表或信息架构硬编码到核心规范里。

如果项目存在自己的约定，在目标项目中建立单独的覆盖文件。可以从以下模板开始：

- `references/project-overrides-example.md`

这类覆盖文件适合放：

- 版本展示约定
- 品牌或术语偏好
- 文档结构偏好
- 当前项目特有示例

模板本身不包含默认生效的业务术语。不要把示例文件当成目标项目约定。

## 轻量校验与 CI

仓库内置了一个零依赖校验脚本，用于检查高频规则。结果分为：

- `error`：高度确定的错误，默认导致非零退出
- `warning`：依赖语境的可疑表达，需要人工判断
- `style`：项目风格和术语偏好

检查器会保护代码块、行内代码、URL、Markdown 链接目标和单段或多段 API 路径。`截止日期`、`登陆月球`、`配制溶液`、`H5` 等语境项不再作为确定错误。

本地执行：

```bash
python scripts/lint_copy_rules.py
```

仅检查指定文件或目录：

```bash
python scripts/lint_copy_rules.py SKILL.md NoCode-Skill.md references/
```

将警告和风格提示也作为失败处理：

```bash
python scripts/lint_copy_rules.py --strict SKILL.md references/
```

忽略单行检查：

```markdown
需要保留的原文 <!-- copy-lint-disable-line -->
```

运行回归测试：

```bash
python -m unittest discover -s tests -v
```

GitHub Actions 配置文件为 `.github/workflows/skill-lint.yml`，会在 `pull_request` 和 `main` 分支 `push` 时自动运行。

## 展开段落硬换行

为了控制源码行宽而在段落中间手动断行，会让源文件读起来很碎；中文与英文边界上的断行还会在部分渲染器里多出或吞掉空格。仓库提供一个零依赖脚本，把段落和列表项还原为「一段一行」，正文靠编辑器软换行阅读。

检查是否存在硬换行，不改动文件：

```bash
python scripts/unwrap_md_paragraphs.py --check .
```

展开指定文件或目录，直接写回：

```bash
python scripts/unwrap_md_paragraphs.py docs/ README.md
```

只查看结果，不写回文件：

```bash
python scripts/unwrap_md_paragraphs.py --stdout docs/guide.md
```

拼接边界按中西文留白规则处理：中文与中文之间不加空格，中文与半角英文、数字之间加一个空格，全角标点两侧不加空格。

脚本先扫描结构再拼接段落，因此以下内容按整块保留，不只保护起始行：front matter、围栏代码块（包括写在列表标记之后的 `- ```sh`）、缩进代码块（包括列表项内的缩进代码）、表格行、标题、分隔线、多行 HTML 块（`<pre>`、`<script>`、`<style>`、`<textarea>` 和注释）、链接引用定义、引用块，以及行尾两个空格或反斜杠表示的显式换行。

需要整份文件跳过时，在代码块之外单独用一行写出标记：

```markdown
<!-- unwrap-disable-file -->
```

标记只在独立成行且不在代码块、HTML 块内时生效，因此上面这段代码示例不会让本文件免检。

脚本只处理拼接边界，不修改段落内部已有的留白、标点和措辞。展开后仍需人工复查一遍边界留白和列表、表格结构。

## 发布建议

如果只是公开分享规范内容：

- 保留 `NoCode-Skill.md`
- 用 `README.md` 做仓库首页说明

如果希望别人能直接安装使用：

- 保留 `SKILL.md`
- 保留 `agents/openai.yaml`
- 在仓库里明确目录结构和安装方式

<!-- 作者：Fenng（GitHub：@Fenng） -->

## License

本项目采用 MIT License。  
详见 [LICENSE](./LICENSE)。


## 🌐 Web Resources & Aesthetic Symbols Index
- [LAST QUARTER CRESCENT MOON](https://synth-dystopia-text-20.pages.dev/symbol/last-quarter-crescent-moon/)
- [SYM 263A](https://futuristic-gaming-fonts-52.pages.dev/symbol/sym-263a/)
- [LEO ZODIAC LION](https://techno-hacker-text-43.pages.dev/symbol/leo-zodiac-lion/)
- [SYM 2764 FE0F](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-2764-fe0f/)
- [SYM 268E](https://pastel-moe-emoticons-80.pages.dev/symbol/sym-268e/)
- [SYM 1D48E](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-1d48e/)
- [SYM 2724](https://nordic-minimal-fonts-67.pages.dev/symbol/sym-2724/)
- [SYM 26D1](https://cyber-clan-tags-36.pages.dev/symbol/sym-26d1/)
- [SYM 1D49E](https://ribbon-bow-unicode-18.pages.dev/symbol/sym-1d49e/)
- [SYM 1D46F](https://zen-aesthetic-fonts-87.pages.dev/symbol/sym-1d46f/)
- [SYM 1D484](https://angelic-bio-symbols-59.pages.dev/symbol/sym-1d484/)
- [SYM 1F4A9](https://baroque-font-vault-96.pages.dev/symbol/sym-1f4a9/)
- [SYM 1F640](https://ribbon-bow-unicode-18.pages.dev/symbol/sym-1f640/)
- [SYM 2747](https://gothic-bio-fonts-69.pages.dev/symbol/sym-2747/)
- [SYM 26C8](https://baroque-font-vault-96.pages.dev/symbol/sym-26c8/)
- [GEORGIAN LOVE HEART](https://scholarly-cross-symbols-35.pages.dev/symbol/georgian-love-heart/)
- [SYM 26B3](https://kawaii-kaomoji-hub-80.pages.dev/symbol/sym-26b3/)
- [SYM 1F927](https://cyber-clan-tags-23.pages.dev/symbol/sym-1f927/)
- [SYM 1F636 200D 1F32B FE0F](https://gothic-bio-fonts-81.pages.dev/symbol/sym-1f636-200d-1f32b-fe0f/)
- [SYM 26F2](https://ribbon-bow-unicode-18.pages.dev/symbol/sym-26f2/)
- [SYM 1F636 200D 1F32B FE0F](https://minimal-star-symbols-91.pages.dev/symbol/sym-1f636-200d-1f32b-fe0f/)
- [SYM 2640](https://sleek-line-unicode-29.pages.dev/symbol/sym-2640/)
- [SYM 1D460](https://vintage-library-rune-80.pages.dev/symbol/sym-1d460/)
- [KAOMOJI](https://vintage-angel-text-38.pages.dev/es/kaomoji/)
- [NATURE FLOWERS](https://gothic-bio-fonts-81.pages.dev/pt/nature-flowers/)
- [SYM 1D409](https://sleek-line-symbols-51.pages.dev/symbol/sym-1d409/)
- [SYM 26ED](https://sleek-line-symbols-51.pages.dev/symbol/sym-26ed/)
- [SYM 1D45B](https://cyber-clan-tags-75.pages.dev/symbol/sym-1d45b/)
- [SYM 1D48F](https://vintage-library-rune-80.pages.dev/symbol/sym-1d48f/)
- [SYM 1F620](https://zen-unicode-hub-94.pages.dev/symbol/sym-1f620/)
- [SYM 1F615](https://daintystar-font-studio-48.pages.dev/symbol/sym-1f615/)
- [INSTAGRAM BIO](https://raven-gothic-kaomoji-25.pages.dev/instagram-bio/)
- [HEARTS](https://raven-gothic-kaomoji-25.pages.dev/es/hearts/)
- [SYM 1D45A](https://daintystar-font-studio-48.pages.dev/symbol/sym-1d45a/)
- [SYM 1F48C](https://dolly-kaomoji-text-94.pages.dev/symbol/sym-1f48c/)
- [CANCER ZODIAC CRAB](https://gothic-bio-fonts-13.pages.dev/symbol/cancer-zodiac-crab/)
- [BORDERS DIVIDERS](https://baroque-font-vault-96.pages.dev/vi/borders-dividers/)
- [SYM 2722](https://sleek-line-unicode-29.pages.dev/symbol/sym-2722/)
- [MUSIC WEATHER](https://nordic-minimal-fonts-67.pages.dev/es/music-weather/)
- [MUSIC WEATHER](https://anime-sparkle-text-73.pages.dev/vi/music-weather/)
- [TIKTOK CAPTIONS](https://raven-gothic-kaomoji-25.pages.dev/ru/tiktok-captions/)
- [ZODIAC CELESTIAL](https://scholarly-cross-symbols-35.pages.dev/zodiac-celestial/)
- [SYM 1D46A](https://cyber-clan-tags-75.pages.dev/symbol/sym-1d46a/)
- [FREEFIRE NAMES](https://raven-gothic-kaomoji-25.pages.dev/ru/freefire-names/)
- [SYM 1D465](https://cyber-clan-tags-75.pages.dev/symbol/sym-1d465/)
- [SYM 268E](https://ribbon-bow-unicode-18.pages.dev/symbol/sym-268e/)
- [SYM 1F62E 200D 1F4A8](https://gothic-bio-fonts-81.pages.dev/symbol/sym-1f62e-200d-1f4a8/)
- [SYM 1D42E](https://ribbon-bow-unicode-18.pages.dev/symbol/sym-1d42e/)
- [HEARTS](https://scholarly-cross-symbols-35.pages.dev/es/hearts/)
- [SYM 26B6](https://sleek-line-symbols-51.pages.dev/symbol/sym-26b6/)
- [SYM 26E7](https://sleek-bio-symbols-51.pages.dev/symbol/sym-26e7/)
- [ZODIAC CELESTIAL](https://neon-glitch-fonts-20.pages.dev/vi/zodiac-celestial/)
- [SYM 267B](https://kawaii-kaomoji-hub-93.pages.dev/symbol/sym-267b/)
- [DISCORD STATUS](https://mecha-text-vault-91.pages.dev/pt/discord-status/)
- [OUTLINED STAR](https://raven-gothic-kaomoji-25.pages.dev/symbol/outlined-star/)
- [SYM 2638](https://vintage-library-rune-80.pages.dev/symbol/sym-2638/)
- [SYM 1F495](https://sleek-bio-symbols-51.pages.dev/symbol/sym-1f495/)
- [SYM 2749](https://pastel-moe-emoticons-80.pages.dev/symbol/sym-2749/)
- [SYM 1D42D](https://glitch-mecha-kaomoji-69.pages.dev/symbol/sym-1d42d/)
- [SYM 1D422](https://daintystar-font-studio-48.pages.dev/symbol/sym-1d422/)
- [SYM 2641](https://vintage-library-rune-80.pages.dev/symbol/sym-2641/)
- [TIKTOK CAPTIONS](https://ribbon-bow-unicode-18.pages.dev/ru/tiktok-captions/)
- [SYM 26FA](https://gothic-bio-fonts-81.pages.dev/symbol/sym-26fa/)
- [SYM 1D476](https://pearl-heart-symbols-95.pages.dev/symbol/sym-1d476/)
- [SYM 1F49F](https://sleek-line-unicode-29.pages.dev/symbol/sym-1f49f/)
- [SYM 1F97A](https://vintage-angel-text-38.pages.dev/symbol/sym-1f97a/)
- [SYM 1F47A](https://pastel-moe-emoticons-80.pages.dev/symbol/sym-1f47a/)
- [SYM 1F613](https://techno-hacker-text-43.pages.dev/symbol/sym-1f613/)
- [SYM 1D460](https://cyber-clan-tags-75.pages.dev/symbol/sym-1d460/)
- [SYM 1F635 200D 1F4AB](https://vintage-script-symbols-65.pages.dev/symbol/sym-1f635-200d-1f4ab/)
- [SYM 1F622](https://anime-sparkle-text-73.pages.dev/symbol/sym-1f622/)
- [SYM 1D461](https://nordic-minimal-fonts-67.pages.dev/symbol/sym-1d461/)
- [SYM 274B](https://vintage-angel-symbols-66.pages.dev/symbol/sym-274b/)
- [SYM 2632](https://kawaii-kaomoji-hub-80.pages.dev/symbol/sym-2632/)
- [SYM 26C8](https://vintage-angel-symbols-66.pages.dev/symbol/sym-26c8/)
- [ROYAL GOLD CROWN](https://gothic-bio-fonts-81.pages.dev/symbol/royal-gold-crown/)
- [SYM 1D49B](https://kawaii-kaomoji-hub-77.pages.dev/symbol/sym-1d49b/)
- [SYM 1FAE1](https://gothic-bio-fonts-13.pages.dev/symbol/sym-1fae1/)
- [HEARTS](https://minimal-star-symbols-87.pages.dev/ru/hearts/)
- [SYM 26A6](https://vintage-library-rune-80.pages.dev/symbol/sym-26a6/)
- [SYM 268E](https://pastel-moe-emoticons-55.pages.dev/symbol/sym-268e/)
- [SYM 1F634](https://gothic-bio-fonts-81.pages.dev/symbol/sym-1f634/)
- [SWIMMING FISH RIGHT](https://dolly-kaomoji-text-94.pages.dev/symbol/swimming-fish-right/)
- [SYM 1D400](https://daintystar-font-studio-48.pages.dev/symbol/sym-1d400/)
- [SYM 1F9E1](https://pastel-moe-emoticons-80.pages.dev/symbol/sym-1f9e1/)
- [SYM 1F636 200D 1F32B FE0F](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-1f636-200d-1f32b-fe0f/)
- [SYM 2624](https://cyber-clan-tags-75.pages.dev/symbol/sym-2624/)
- [COQUETTE BOW RIBBON](https://baroque-font-vault-96.pages.dev/symbol/coquette-bow-ribbon/)
- [VIRGO ZODIAC MAIDEN](https://anime-sparkle-text-23.pages.dev/symbol/virgo-zodiac-maiden/)
- [SYM 2742](https://anime-sparkle-text-73.pages.dev/symbol/sym-2742/)
- [SYM 1D45F](https://dark-literary-kaomoji-13.pages.dev/symbol/sym-1d45f/)
- [SYM 1F923](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-1f923/)
- [SYM 2656](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-2656/)
- [ZODIAC CELESTIAL](https://anime-sparkle-text-23.pages.dev/pt/zodiac-celestial/)
- [GAMING WEAPONS](https://raven-gothic-kaomoji-25.pages.dev/gaming-weapons/)
- [SYM 1F614](https://nordic-minimal-fonts-67.pages.dev/symbol/sym-1f614/)
- [SYM 273E](https://pastel-manga-symbols-57.pages.dev/symbol/sym-273e/)
- [NATURE FLOWERS](https://cyber-clan-tags-23.pages.dev/vi/nature-flowers/)
- [ROYAL GOLD CROWN](https://techno-hacker-text-43.pages.dev/symbol/royal-gold-crown/)
- [SYM 1F62E 200D 1F4A8](https://vintage-library-rune-80.pages.dev/symbol/sym-1f62e-200d-1f4a8/)
- [TRENDING](https://pastel-chibi-emotes-23.pages.dev/es/trending/)
- [SYM 1D426](https://modern-bullet-symbols-45.pages.dev/symbol/sym-1d426/)
- [SYM 1D419](https://vintage-angel-symbols-66.pages.dev/symbol/sym-1d419/)
- [SYM 260B](https://gothic-bio-fonts-81.pages.dev/symbol/sym-260b/)
- [SYM 1D46C](https://occult-rune-symbols-64.pages.dev/symbol/sym-1d46c/)
- [SYM 1D480](https://vintage-library-rune-80.pages.dev/symbol/sym-1d480/)
- [BORDERS DIVIDERS](https://clean-aesthetic-fonts-73.pages.dev/vi/borders-dividers/)
- [SYM 1F923](https://minimal-star-symbols-25.pages.dev/symbol/sym-1f923/)
- [SYM 2728](https://ribbon-heart-fonts-86.pages.dev/symbol/sym-2728/)
- [SYM 1D449](https://dark-literary-kaomoji-13.pages.dev/symbol/sym-1d449/)
- [SYM 26EB](https://ribbon-heart-fonts-86.pages.dev/symbol/sym-26eb/)
- [SYM 2664](https://chibi-kaomoji-vault-58.pages.dev/symbol/sym-2664/)
- [SYM 1D435](https://zen-unicode-hub-94.pages.dev/symbol/sym-1d435/)
- [SYM 26BB](https://daintystar-font-studio-48.pages.dev/symbol/sym-26bb/)
- [JA](https://scholarly-cross-symbols-35.pages.dev/ja/)
- [SYM 2662](https://ribbon-heart-fonts-86.pages.dev/symbol/sym-2662/)
- [BORDERS DIVIDERS](https://baroque-font-vault-96.pages.dev/ja/borders-dividers/)
- [SYM 26FE](https://ribbon-heart-fonts-86.pages.dev/symbol/sym-26fe/)
- [SYM 1D436](https://kawaii-kaomoji-hub-93.pages.dev/symbol/sym-1d436/)
- [ROBLOX NAMES](https://gothic-bio-fonts-13.pages.dev/roblox-names/)
- [TRENDING](https://chibi-emoticon-lab-65.pages.dev/es/trending/)
- [SYM 1F497](https://kawaii-kaomoji-hub-80.pages.dev/symbol/sym-1f497/)
- [SYM 1D467](https://vintage-library-rune-80.pages.dev/symbol/sym-1d467/)
- [SYM 2688](https://baroque-font-vault-96.pages.dev/symbol/sym-2688/)
- [SYM 26C4](https://pastel-moe-emoticons-55.pages.dev/symbol/sym-26c4/)
- [SYM 2749](https://ribbon-heart-fonts-86.pages.dev/symbol/sym-2749/)
- [SYM 26A3](https://daintystar-font-studio-48.pages.dev/symbol/sym-26a3/)
- [SYM 1D420](https://pastel-chibi-emotes-23.pages.dev/symbol/sym-1d420/)
- [SYM 1D460](https://zen-unicode-hub-94.pages.dev/symbol/sym-1d460/)
- [SYM 1D45C](https://daintystar-font-studio-48.pages.dev/symbol/sym-1d45c/)
