"""Tests for `langgraph.stream.StreamChannel` name validation."""

from __future__ import annotations

import pytest

from langgraph.stream.stream_channel import StreamChannel


def test_rejects_empty_name() -> None:
    """Empty `name` would produce malformed `custom:` protocol events in StreamMux."""
    with pytest.raises(ValueError, match="`name` must be a non-empty string"):
        StreamChannel(name="")


def test_rejects_non_string_name() -> None:
    """Non-string `name` would break the `f\"custom:{value.name}\"` string interpolation."""
    with pytest.raises(TypeError, match="`name` must be a string or None"):
        StreamChannel(name=42)  # type: ignore[arg-type]


def test_accepts_none_name() -> None:
    """`name=None` is the local-only channel mode and works without validation."""
    channel = StreamChannel(name=None)
    assert channel.name is None


def test_accepts_non_empty_name() -> None:
    """Valid non-empty string `name` produces a working channel."""
    channel = StreamChannel(name="lifecycle")
    assert channel.name == "lifecycle"
