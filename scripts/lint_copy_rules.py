#!/usr/bin/env python3
"""轻量文案规则校验。

默认检查：
1) 可见正文中不允许使用 ASCII 双引号和中文弯引号
2) 可见正文中不允许使用「你 / 您 / 同学」
3) 高频术语大小写归一（ID / HTTP / URL / JSON / API / AI）

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

DEFAULT_FILES = [
    "SKILL.md",
    "NoCode-Skill.md",
    "README.md",
    "references/Project-Overrides.md",
]

FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
URL_RE = re.compile(r"https?://\S+")
API_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_])/[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)+(?![A-Za-z0-9_])"
)

FORBIDDEN_QUOTES = {
    '"': "ASCII 双引号",
    "“": "中文弯引号",
    "”": "中文弯引号",
}

FORBIDDEN_ADDRESS = ["你", "您", "同学"]

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
    visible = mask_match(visible, URL_RE)
    visible = mask_match(visible, API_PATH_RE)
    return visible


def scan_markdown(path: Path) -> list[Violation]:
    violations: list[Violation] = []
    in_fence = False

    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
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

        for term in FORBIDDEN_ADDRESS:
            for match in re.finditer(re.escape(term), visible):
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

    return violations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验中文技术文案高频规则")
    parser.add_argument(
        "files",
        nargs="*",
        help="要检查的 Markdown 文件；为空时使用默认文件集合",
    )
    return parser.parse_args()


def collect_targets(args: argparse.Namespace) -> list[Path]:
    raw_targets = args.files if args.files else DEFAULT_FILES
    targets: list[Path] = []

    for item in raw_targets:
        path = Path(item)
        if not path.exists():
            print(f"[WARN] 文件不存在，已跳过: {item}", file=sys.stderr)
            continue
        if path.is_dir():
            targets.extend(sorted(path.rglob("*.md")))
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
