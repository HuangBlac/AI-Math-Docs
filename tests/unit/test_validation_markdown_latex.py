from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ai_math_study.validation import validate_note  # noqa: E402


def error_codes(markdown: str) -> set[str]:
    return {issue.code for issue in validate_note(markdown) if issue.severity == "error"}


class MarkdownLatexValidationTests(unittest.TestCase):
    def test_valid_note_passes_and_ignores_code_contents(self) -> None:
        markdown = r"""# 标题

## 定义

行内公式 $R(f)=\mathbb E[\ell(Y,f(X))]$。

### 说明

$$
\begin{aligned}
R(f) &= \mathbb E[\ell(Y,f(X))] \\
&\leq \left\lVert f \right\rVert.
\end{aligned}
$$

```text
$ broken
\left \begin{ignored}
```
"""
        self.assertEqual(error_codes(markdown), set())

    def test_requires_exactly_one_h1(self) -> None:
        self.assertIn("markdown_h1_count", error_codes("## 小节\n"))
        self.assertIn("markdown_h1_count", error_codes("# 一\n\n# 二\n"))

    def test_rejects_heading_level_jump(self) -> None:
        self.assertIn("markdown_heading_jump", error_codes("# 标题\n\n### 跳级\n"))

    def test_rejects_unbalanced_dollar_delimiter(self) -> None:
        self.assertIn("latex_dollar_unbalanced", error_codes("# 标题\n\n错误 $x+y。\n"))

    def test_rejects_unbalanced_left_right(self) -> None:
        self.assertIn("latex_left_right", error_codes(r"# 标题" "\n\n$\\left(x+y$\n"))

    def test_rejects_mismatched_begin_end(self) -> None:
        markdown = r"""# 标题

$$
\begin{aligned}
x &= y
\end{cases}
$$
"""
        self.assertIn("latex_environment", error_codes(markdown))

    def test_rejects_unresolved_protection_token(self) -> None:
        markdown = "# 标题\n\n@@AIMATH_INLINE_CODE_0001_deadbeefdead@@\n"
        self.assertIn("protected_token_unresolved", error_codes(markdown))


if __name__ == "__main__":
    unittest.main()
