from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from typing import Protocol


_AssertionTextDiffStyle = Literal["ndiff", "block"]


@dataclass(frozen=True, kw_only=True, slots=True)
class TruncationBudget:
    """Per-explanation budget for truncating assertion output.

    ``max_lines`` / ``max_chars`` mirror the ``truncation_limit_lines`` /
    ``truncation_limit_chars`` ini values: a positive limit bounds that
    dimension; ``0`` leaves it unbounded (the limit is disabled).
    """

    max_lines: int
    max_chars: int

    def as_pformat_bounds(self) -> tuple[int | None, int | None]:
        """Return ``(max_lines, max_chars)`` for ``PrettyPrinter.pformat_lines``.

        That API spells an unbounded dimension as ``None``; this budget
        spells it ``0``.
        """
        return self.max_lines or None, self.max_chars or None

    def cap_chars(self, text: str) -> str:
        """Clip ``text`` to ``max_chars`` (``0`` leaves it unbounded)."""
        return text[: self.max_chars] if self.max_chars > 0 else text

    def cap_lines(self, lines: list[str]) -> list[str]:
        """Clip ``lines`` to ``max_lines`` (``0`` leaves it unbounded)."""
        return lines[: self.max_lines] if self.max_lines > 0 else lines


# Reusable "no cap" budget, used as a default argument (B008).
NO_TRUNCATION_BUDGET = TruncationBudget(max_lines=0, max_chars=0)


class _HighlightFunc(Protocol):  # noqa: PYI046
    def __call__(self, source: str, lexer: Literal["diff", "python"] = "python") -> str:
        """Apply highlighting to the given source."""
