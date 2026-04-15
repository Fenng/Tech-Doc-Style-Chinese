#!/usr/bin/env python3
"""轻量文案规则校验。

默认检查：
1) 可见正文中不允许使用 ASCII 双引号和中文弯引号
2) 可见正文中不允许使用「你 / 您 / 同学」
3) 高频术语大小写归一（ID / HTTP / URL / JSON / API / AI）
4) 指定缩写禁用（JS / Js / H5）
5) AI 术语误写（LLM / AIGC / RAG / ChatGPT / OpenAI API 等）
6) 中文高频错词（阀值 / 登陆 / 布署 / 配制 等）

说明：
- 这是轻量脚本，不做完整 Markdown 语法解析。
- 会忽略 fenced code block、行内代码、URL 与常见 API 路径。
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TARGETS = ["."]

FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
URL_RE = re.compile(r"https?://\S+")
API_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_])/[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)+(?![A-Za-z0-9_])"
)
INLINE_LINK_RE = re.compile(r"(!?\[[^\]]*]\()([^)]+)(\))")

FORBIDDEN_QUOTES = {
    '"': "ASCII 双引号",
    "“": "中文弯引号",
    "”": "中文弯引号",
}

NON_WORD_CHARS = r"\u4e00-\u9fffA-Za-z0-9_"
PREFIX_CONTEXT_CHARS = "与跟对向给帮替为请让"
SUFFIX_HINTS = "可会要能应需请把将来去做看读写用"

FORBIDDEN_ADDRESS_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # 「你」：独立词起始（前面不是中文/字母/数字）或在「与你」等上下文中。
    (
        re.compile(
            rf"(?<![{NON_WORD_CHARS}])你(?=$|[^\u4e00-\u9fff]|[{SUFFIX_HINTS}])"
        ),
        "你",
    ),
    (re.compile(rf"(?<=[{PREFIX_CONTEXT_CHARS}])你"), "你"),
    # 「您」基本不会作为其他词片段出现，直接命中。
    (re.compile(r"您"), "您"),
    # 「同学」按词组命中，覆盖「同学们」「欢迎同学」等常见称呼。
    (re.compile(r"同学(?:们|們)?"), "同学"),
]

SKIP_DIR_NAMES = {".git"}

CASE_RULES = [
    (re.compile(r"(?<![A-Za-z0-9_])id(?![A-Za-z0-9_])"), "ID"),
    (re.compile(r"(?<![A-Za-z0-9_])Id(?![A-Za-z0-9_])"), "ID"),
    (re.compile(r"(?<![A-Za-z0-9_])http(?![A-Za-z0-9_])"), "HTTP"),
    (re.compile(r"(?<![A-Za-z0-9_])Http(?![A-Za-z0-9_])"), "HTTP"),
    (re.compile(r"(?<![A-Za-z0-9_])url(?![A-Za-z0-9_])"), "URL"),
    (re.compile(r"(?<![A-Za-z0-9_])Url(?![A-Za-z0-9_])"), "URL"),
    (re.compile(r"(?<![A-Za-z0-9_])json(?![A-Za-z0-9_])"), "JSON"),
    (re.compile(r"(?<![A-Za-z0-9_])Json(?![A-Za-z0-9_])"), "JSON"),
    (re.compile(r"(?<![A-Za-z0-9_])api(?![A-Za-z0-9_])"), "API"),
    (re.compile(r"(?<![A-Za-z0-9_])Api(?![A-Za-z0-9_])"), "API"),
    (re.compile(r"(?<![A-Za-z0-9_])ai(?![A-Za-z0-9_])"), "AI"),
    (re.compile(r"(?<![A-Za-z0-9_])Ai(?![A-Za-z0-9_])"), "AI"),
]

ABBREVIATION_RULES = [
    (re.compile(r"(?<![A-Za-z0-9_])JS(?![A-Za-z0-9_])"), "JavaScript"),
    (re.compile(r"(?<![A-Za-z0-9_])Js(?![A-Za-z0-9_])"), "JavaScript"),
    (re.compile(r"(?<![A-Za-z0-9_])H5(?![A-Za-z0-9_])"), "HTML5"),
]

AI_TERM_RULES = [
    (re.compile(r"(?<![A-Za-z0-9_])llm(?![A-Za-z0-9_])"), "LLM"),
    (re.compile(r"(?<![A-Za-z0-9_])Llm(?![A-Za-z0-9_])"), "LLM"),
    (re.compile(r"(?<![A-Za-z0-9_])aigc(?![A-Za-z0-9_])"), "AIGC"),
    (re.compile(r"(?<![A-Za-z0-9_])Aigc(?![A-Za-z0-9_])"), "AIGC"),
    (re.compile(r"(?<![A-Za-z0-9_])rag(?![A-Za-z0-9_])"), "RAG"),
    (re.compile(r"(?<![A-Za-z0-9_])Rag(?![A-Za-z0-9_])"), "RAG"),
    (re.compile(r"(?<![A-Za-z0-9_])chatgpt(?![A-Za-z0-9_])"), "ChatGPT"),
    (re.compile(r"(?<![A-Za-z0-9_])Chatgpt(?![A-Za-z0-9_])"), "ChatGPT"),
    (re.compile(r"(?<![A-Za-z0-9_])openai\\s+api(?![A-Za-z0-9_])"), "OpenAI API"),
    (re.compile(r"(?<![A-Za-z0-9_])OpenAI\\s+api(?![A-Za-z0-9_])"), "OpenAI API"),
    (re.compile(r"(?<![A-Za-z0-9_])embeding(?![A-Za-z0-9_])"), "embedding"),
    (re.compile(r"(?<![A-Za-z0-9_])finetune(?![A-Za-z0-9_])"), "fine-tuning"),
    (re.compile(r"(?<![A-Za-z0-9_])fine\\s+tune(?![A-Za-z0-9_])"), "fine-tuning"),
    (re.compile(r"提示工程学"), "提示工程"),
    (re.compile(r"幻听"), "幻觉"),
]

TYPO_RULES = [
    (re.compile(r"阀值"), "阈值"),
    (re.compile(r"登陆"), "登录"),
    (re.compile(r"布署"), "部署"),
    (re.compile(r"配制"), "配置"),
    (re.compile(r"起用"), "启用"),
    (re.compile(r"反回"), "返回"),
    (re.compile(r"回朔"), "回溯"),
    (re.compile(r"标示"), "标识"),
    (re.compile(r"帐户"), "账户"),
    (re.compile(r"帐号"), "账号"),
    (re.compile(r"截止"), "截至"),
    (re.compile(r"搜寻"), "搜索"),
    # 「即时」仅在技术语境下提示为「实时」，避免误报到通用语境。
    (
        re.compile(
            r"即时(?=(通信|消息|处理|监控|更新|同步|计算|响应|数据|日志|推送|渲染|指标|告警|检索|查询|任务|分析|流式|调用|服务|接口|系统))"
        ),
        "实时",
    ),
    (re.compile(r"做为"), "作为"),
]


@dataclass
class Violation:
    file: Path
    line: int
    col: int
    kind: str
    message: str
    snippet: str


def mask_match(text: str, regex: re.Pattern[str]) -> str:
    def replacer(match: re.Match[str]) -> str:
        return " " * (match.end() - match.start())

    return regex.sub(replacer, text)


def prepare_visible_line(line: str) -> str:
    visible = line
    visible = mask_match(visible, INLINE_CODE_RE)
    visible = INLINE_LINK_RE.sub(
        lambda m: f"{m.group(1)}{' ' * len(m.group(2))}{m.group(3)}", visible
    )
    visible = mask_match(visible, URL_RE)
    visible = mask_match(visible, API_PATH_RE)
    return visible


def iter_forbidden_address_matches(line: str):
    seen: set[tuple[int, int, str]] = set()
    for pattern, label in FORBIDDEN_ADDRESS_PATTERNS:
        for match in pattern.finditer(line):
            key = (match.start(), match.end(), label)
            if key in seen:
                continue
            seen.add(key)
            yield match, label


def scan_markdown(path: Path) -> list[Violation]:
    violations: list[Violation] = []
    in_fence = False
    lines = path.read_text(encoding="utf-8").splitlines()
    in_front_matter = bool(lines and lines[0].strip() == "---")

    for line_no, raw in enumerate(lines, start=1):
        # Ignore YAML front matter block at file head.
        if in_front_matter:
            if line_no != 1 and raw.strip() in {"---", "..."}:
                in_front_matter = False
            continue

        if FENCE_RE.match(raw):
            in_fence = not in_fence
            continue

        if in_fence:
            continue

        visible = prepare_visible_line(raw)

        for quote, label in FORBIDDEN_QUOTES.items():
            for match in re.finditer(re.escape(quote), visible):
                violations.append(
                    Violation(
                        file=path,
                        line=line_no,
                        col=match.start() + 1,
                        kind="quote",
                        message=f"可见正文包含 {label}，请改为直角引号「」或移入代码环境",
                        snippet=raw.strip(),
                    )
                )

        for match, term in iter_forbidden_address_matches(visible):
            violations.append(
                Violation(
                    file=path,
                    line=line_no,
                    col=match.start() + 1,
                    kind="address",
                    message=f"可见正文包含禁用称呼「{term}」",
                    snippet=raw.strip(),
                )
            )

        for pattern, suggested in CASE_RULES:
            for match in pattern.finditer(visible):
                wrong = match.group(0)
                violations.append(
                    Violation(
                        file=path,
                        line=line_no,
                        col=match.start() + 1,
                        kind="casing",
                        message=f"术语「{wrong}」建议改为「{suggested}」",
                        snippet=raw.strip(),
                    )
                )

        for pattern, suggested in ABBREVIATION_RULES:
            for match in pattern.finditer(visible):
                wrong = match.group(0)
                violations.append(
                    Violation(
                        file=path,
                        line=line_no,
                        col=match.start() + 1,
                        kind="abbreviation",
                        message=f"缩写「{wrong}」建议改为「{suggested}」",
                        snippet=raw.strip(),
                    )
                )

        for pattern, suggested in AI_TERM_RULES:
            for match in pattern.finditer(visible):
                wrong = match.group(0)
                violations.append(
                    Violation(
                        file=path,
                        line=line_no,
                        col=match.start() + 1,
                        kind="ai-term",
                        message=f"AI 术语「{wrong}」建议改为「{suggested}」",
                        snippet=raw.strip(),
                    )
                )

        for pattern, suggested in TYPO_RULES:
            for match in pattern.finditer(visible):
                wrong = match.group(0)
                violations.append(
                    Violation(
                        file=path,
                        line=line_no,
                        col=match.start() + 1,
                        kind="typo",
                        message=f"词语「{wrong}」建议改为「{suggested}」",
                        snippet=raw.strip(),
                    )
                )

    return violations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验中文技术文案高频规则")
    parser.add_argument(
        "files",
        nargs="*",
        help="要检查的 Markdown 文件或目录；为空时默认检查当前目录下所有 Markdown 文件",
    )
    return parser.parse_args()


def collect_targets(args: argparse.Namespace) -> list[Path]:
    raw_targets = args.files if args.files else DEFAULT_TARGETS
    targets: list[Path] = []

    for item in raw_targets:
        path = Path(item)
        if not path.exists():
            print(f"[WARN] 文件不存在，已跳过: {item}", file=sys.stderr)
            continue
        if path.is_dir():
            for markdown in sorted(path.rglob("*.md")):
                if any(part in SKIP_DIR_NAMES for part in markdown.parts):
                    continue
                targets.append(markdown)
        else:
            targets.append(path)

    deduped = sorted({path.resolve(): path for path in targets}.values(), key=lambda p: str(p))
    return deduped


def main() -> int:
    args = parse_args()
    targets = collect_targets(args)

    if not targets:
        print("未找到可检查的 Markdown 文件。", file=sys.stderr)
        return 1

    all_violations: list[Violation] = []
    for target in targets:
        all_violations.extend(scan_markdown(target))

    if not all_violations:
        print(f"PASS: 共检查 {len(targets)} 个文件，未发现违规项。")
        return 0

    print(f"FAIL: 共检查 {len(targets)} 个文件，发现 {len(all_violations)} 个违规项：")
    for item in all_violations:
        print(
            f"- {item.file}:{item.line}:{item.col} [{item.kind}] {item.message}\n"
            f"  {item.snippet}"
        )
    return 2


if __name__ == "__main__":
    sys.exit(main())
