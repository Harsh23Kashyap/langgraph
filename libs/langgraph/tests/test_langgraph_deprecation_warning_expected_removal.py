"""Tests for `langgraph.warnings.LangGraphDeprecationWarning.expected_removal` validation."""

from __future__ import annotations

import pytest

from langgraph.warnings import LangGraphDeprecationWarning


def test_rejects_short_expected_removal() -> None:
    """`expected_removal` of length 1 would IndexError at `self.expected_removal[1]` in `__str__`."""
    with pytest.raises(
        ValueError,
        match="`expected_removal` must be a 2-tuple of \\(major, minor\\)",
    ):
        LangGraphDeprecationWarning("deprecated", since=(0, 5), expected_removal=(1,))  # type: ignore[arg-type]


def test_rejects_empty_expected_removal() -> None:
    """Empty `expected_removal` would IndexError at `self.expected_removal[0]` in `__str__`."""
    with pytest.raises(
        ValueError,
        match="`expected_removal` must be a 2-tuple of \\(major, minor\\)",
    ):
        LangGraphDeprecationWarning("deprecated", since=(0, 5), expected_removal=())  # type: ignore[arg-type]


def test_rejects_three_tuple_expected_removal() -> None:
    """`expected_removal` of length 3 would silently ignore the trailing element."""
    with pytest.raises(
        ValueError,
        match="`expected_removal` must be a 2-tuple of \\(major, minor\\)",
    ):
        LangGraphDeprecationWarning(
            "deprecated",
            since=(0, 5),
            expected_removal=(1, 0, 99),  # type: ignore[arg-type]
        )


def test_accepts_none_expected_removal() -> None:
    """`expected_removal=None` is the documented default and triggers the `(since[0] + 1, 0)` fallback."""
    warning = LangGraphDeprecationWarning("deprecated", since=(0, 5))
    assert warning.expected_removal == (1, 0)


def test_accepts_valid_expected_removal() -> None:
    """Valid 2-tuple `expected_removal` overrides the default fallback."""
    warning = LangGraphDeprecationWarning(
        "deprecated", since=(0, 5), expected_removal=(2, 0)
    )
    assert warning.expected_removal == (2, 0)
