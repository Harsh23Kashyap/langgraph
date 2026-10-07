"""Tests for `langgraph.warnings.LangGraphDeprecationWarning` validation."""

from __future__ import annotations

import pytest

from langgraph.warnings import LangGraphDeprecationWarning


def test_rejects_empty_message() -> None:
    """Empty `message` would produce a malformed `__str__` with leading period."""
    with pytest.raises(ValueError, match="`message` must be a non-empty string"):
        LangGraphDeprecationWarning("", since=(0, 5))


def test_rejects_non_string_message() -> None:
    """Non-string `message` would break `rstrip` and `__str__` interpolation."""
    with pytest.raises(TypeError, match="`message` must be a string"):
        LangGraphDeprecationWarning(None, since=(0, 5))  # type: ignore[arg-type]


def test_rejects_short_since() -> None:
    """`since` of length != 2 would IndexError at `self.since[1]` in `__str__`."""
    with pytest.raises(
        ValueError, match="`since` must be a 2-tuple of \\(major, minor\\)"
    ):
        LangGraphDeprecationWarning("deprecated", since=(0,))  # type: ignore[arg-type]


def test_rejects_empty_since() -> None:
    """Empty `since` would IndexError at line 40 (`since[0] + 1`)."""
    with pytest.raises(
        ValueError, match="`since` must be a 2-tuple of \\(major, minor\\)"
    ):
        LangGraphDeprecationWarning("deprecated", since=())  # type: ignore[arg-type]


def test_accepts_valid_arguments() -> None:
    """Valid `message` and `since` arguments produce a working warning."""
    warning = LangGraphDeprecationWarning("deprecated", since=(0, 5))
    assert warning.message == "deprecated"
    assert warning.since == (0, 5)
    assert warning.expected_removal == (1, 0)  # default: (since[0] + 1, 0)


def test_accepts_valid_arguments_with_explicit_expected_removal() -> None:
    """Explicit `expected_removal` overrides the default fallback."""
    warning = LangGraphDeprecationWarning(
        "deprecated", since=(0, 5), expected_removal=(2, 0)
    )
    assert warning.expected_removal == (2, 0)
