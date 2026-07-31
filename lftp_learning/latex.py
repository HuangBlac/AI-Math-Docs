from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
import re


@dataclass(frozen=True)
class ProtectedBlock:
    token: str
    kind: str
    text: str
    sha256: str


@dataclass(frozen=True)
class AuditIssue:
    severity: str
    code: str
    message: str
    token: str | None = None


_BLOCK_PATTERN = re.compile(
    r"(?P<frontmatter>\A---\s*\n.*?\n---\s*(?:\n|\Z))"
    r"|(?P<fence>^(?:```|~~~)[^\n]*\n.*?^(?:```|~~~)\s*$)"
    r"|(?P<display_dollar>\$\$.*?\$\$)"
    r"|(?P<display_bracket>\\\[.*?\\\])"
    r"|(?P<inline_paren>\\\(.*?\\\))"
    r"|(?P<inline_dollar>(?<!\\)(?<!\$)\$(?!\$)(?:\\.|[^$\n])+?(?<!\\)\$(?!\$))",
    re.MULTILINE | re.DOTALL,
)


def protect_sensitive_blocks(markdown: str) -> tuple[str, list[ProtectedBlock]]:
    blocks: list[ProtectedBlock] = []

    def replace(match: re.Match[str]) -> str:
        text = match.group(0)
        kind = match.lastgroup or "unknown"
        digest = sha256(text.encode("utf-8")).hexdigest()
        token = f"@@LFTP_{kind.upper()}_{len(blocks):04d}_{digest[:10]}@@"
        blocks.append(ProtectedBlock(token=token, kind=kind, text=text, sha256=digest))
        return token

    return _BLOCK_PATTERN.sub(replace, markdown), blocks


def restore_sensitive_blocks(protected: str, blocks: list[ProtectedBlock]) -> str:
    result = protected
    for block in blocks:
        count = result.count(block.token)
        if count != 1:
            raise ValueError(f"Protected token {block.token} occurs {count} times; expected exactly once")
        result = result.replace(block.token, block.text)
    leftovers = re.findall(r"@@LFTP_[A-Z_]+_\d{4}_[0-9a-f]{10}@@", result)
    if leftovers:
        raise ValueError(f"Unresolved protected tokens: {leftovers[:3]}")
    return result


def protected_block_fingerprint(blocks: list[ProtectedBlock]) -> Counter[tuple[str, str]]:
    return Counter((block.kind, block.sha256) for block in blocks)


def _balanced_braces(text: str) -> bool:
    depth = 0
    escaped = False
    for char in text:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def _environment_issues(text: str, token: str | None) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    stack: list[str] = []
    for match in re.finditer(r"\\(begin|end)\{([^{}]+)\}", text):
        operation, environment = match.groups()
        if operation == "begin":
            stack.append(environment)
        elif not stack or stack[-1] != environment:
            issues.append(AuditIssue("error", "latex_environment", f"Unmatched \\end{{{environment}}}", token))
        else:
            stack.pop()
    for environment in reversed(stack):
        issues.append(AuditIssue("error", "latex_environment", f"Missing \\end{{{environment}}}", token))
    return issues


def audit_latex(markdown: str) -> list[AuditIssue]:
    _, blocks = protect_sensitive_blocks(markdown)
    issues: list[AuditIssue] = []
    math_kinds = {"display_dollar", "display_bracket", "inline_paren", "inline_dollar"}
    for block in blocks:
        if block.kind not in math_kinds:
            continue
        if not _balanced_braces(block.text):
            issues.append(AuditIssue("error", "latex_braces", "Unbalanced LaTeX braces", block.token))
        if len(re.findall(r"\\left\b", block.text)) != len(re.findall(r"\\right\b", block.text)):
            issues.append(AuditIssue("error", "latex_left_right", "Unbalanced \\left and \\right", block.token))
        if re.search(r"\\exist\b", block.text):
            issues.append(AuditIssue("warning", "latex_command", "Use \\exists instead of \\exist", block.token))
        issues.extend(_environment_issues(block.text, block.token))
    if markdown.count("```") % 2:
        issues.append(AuditIssue("error", "markdown_fence", "Unbalanced triple-backtick code fence"))
    return issues


def apply_safe_latex_fixes(markdown: str) -> str:
    """Apply only syntax-preserving corrections with an unambiguous intent."""
    return re.sub(r"\\exist\b", r"\\exists", markdown)

