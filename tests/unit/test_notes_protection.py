from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ai_math_study.notes.protection import (  # noqa: E402
    ProtectedTokenError,
    protect_markdown,
    restore_markdown,
    validate_token_bijection,
)


class MarkdownProtectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.markdown = r"""---
title: 测试笔记
tags: [lftp]
---

# 主标题

链接 [[rademacher-complexity|Rademacher 复杂度]]，代码 `x = $5`，公式 $R(f)$。

$$
\mathbb{E}[X] = \int x\,dP(x)
$$

\[
\left\lVert x \right\rVert_2^2
\]

```python
price = "$5"
print(r"\\begin{fake}")
```
"""

    def test_round_trip_preserves_every_sensitive_block_byte_for_byte(self) -> None:
        bundle = protect_markdown(self.markdown)

        kinds = {block.kind for block in bundle.blocks}
        self.assertTrue(
            {"frontmatter", "fenced_code", "inline_code", "wikilink", "inline_math", "block_math"}
            <= kinds
        )
        for block in bundle.blocks:
            self.assertNotIn(block.content, bundle.protected_text)
            self.assertEqual(bundle.protected_text.count(block.token), 1)

        self.assertEqual(restore_markdown(bundle.protected_text, bundle), self.markdown)

    def test_missing_or_duplicate_token_is_rejected(self) -> None:
        bundle = protect_markdown(self.markdown)
        token = bundle.blocks[0].token

        with self.assertRaisesRegex(ProtectedTokenError, "missing"):
            restore_markdown(bundle.protected_text.replace(token, "", 1), bundle)

        with self.assertRaisesRegex(ProtectedTokenError, "duplicate"):
            restore_markdown(bundle.protected_text + token, bundle)

    def test_unknown_unrestored_token_is_rejected(self) -> None:
        bundle = protect_markdown(self.markdown)
        tampered = bundle.protected_text + "\n@@AIMATH_INLINE_MATH_9999_deadbeefdead@@\n"

        issues = validate_token_bijection(tampered, bundle)
        self.assertIn("protected_token_unknown", {issue.code for issue in issues})
        with self.assertRaises(ProtectedTokenError):
            restore_markdown(tampered, bundle)


if __name__ == "__main__":
    unittest.main()
