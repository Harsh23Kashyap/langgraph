"""Tests for `langgraph.errors.NodeError` dataclass validation."""

from __future__ import annotations

import pytest

from langgraph.errors import NodeError


def test_rejects_empty_node() -> None:
    """Empty `node` would silently accept a malformed `NodeError` with no node name."""
    with pytest.raises(ValueError, match="`node` must be a non-empty string"):
        NodeError("", ValueError("inner"))


def test_rejects_non_string_node() -> None:
    """Non-string `node` would break the `f\"recovered from {error.node}: ...\"` template."""
    with pytest.raises(TypeError, match="`node` must be a string"):
        NodeError(None, ValueError("inner"))  # type: ignore[arg-type]


def test_rejects_non_exception_error() -> None:
    """Non-BaseException `error` would silently accept a string/int/etc. as the failed exception."""
    with pytest.raises(TypeError, match="`error` must be a BaseException"):
        NodeError("worker", "oops")  # type: ignore[arg-type]


def test_accepts_valid_arguments() -> None:
    """Valid `node` and `error` arguments produce a working NodeError."""
    inner = ValueError("something failed")
    error = NodeError("worker", inner)
    assert error.node == "worker"
    assert error.error is inner


def test_accepts_exception_subclass() -> None:
    """Any BaseException subclass instance (e.g., KeyError, RuntimeError) is accepted."""
    error = NodeError("worker", KeyError("missing key"))
    assert error.node == "worker"
    assert isinstance(error.error, KeyError)
