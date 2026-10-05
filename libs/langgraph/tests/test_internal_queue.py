"""Tests for the SyncQueue bool/non-int timeout guard."""

import queue

import pytest

from langgraph._internal._queue import SyncQueue


def test_sync_queue_get_bool_timeout_raises() -> None:
    """SyncQueue.get rejects bool timeout=True (True == 1 would silently pass)."""
    q: SyncQueue = SyncQueue()
    with pytest.raises(
        TypeError,
        match=r"'timeout' must be a non-negative number, not bool",
    ):
        q.get(timeout=True)


def test_sync_queue_get_string_timeout_raises() -> None:
    """SyncQueue.get rejects str timeout (locks to numeric type)."""
    q: SyncQueue = SyncQueue()
    with pytest.raises(
        TypeError,
        match=r"'timeout' must be a non-negative number, not str",
    ):
        q.get(timeout="1.0")  # type: ignore[arg-type]


def test_sync_queue_get_list_timeout_raises() -> None:
    """SyncQueue.get rejects list timeout."""
    q: SyncQueue = SyncQueue()
    with pytest.raises(
        TypeError,
        match=r"'timeout' must be a non-negative number, not list",
    ):
        q.get(timeout=[1.0])  # type: ignore[arg-type]


def test_sync_queue_get_accepts_zero_int_timeout() -> None:
    """SyncQueue.get accepts 0 timeout (sanity check)."""
    q: SyncQueue = SyncQueue()
    with pytest.raises(queue.Empty):
        q.get(block=True, timeout=0)


def test_sync_queue_get_accepts_float_timeout() -> None:
    """SyncQueue.get accepts float timeout (sanity check)."""
    q: SyncQueue = SyncQueue()
    with pytest.raises(queue.Empty):
        q.get(block=True, timeout=0.5)


def test_sync_queue_wait_bool_timeout_raises() -> None:
    """SyncQueue.wait rejects bool timeout=True."""
    q: SyncQueue = SyncQueue()
    with pytest.raises(
        TypeError,
        match=r"'timeout' must be a non-negative number, not bool",
    ):
        q.wait(timeout=True)


def test_sync_queue_wait_string_timeout_raises() -> None:
    """SyncQueue.wait rejects str timeout (locks to numeric type)."""
    q: SyncQueue = SyncQueue()
    with pytest.raises(
        TypeError,
        match=r"'timeout' must be a non-negative number, not str",
    ):
        q.wait(timeout="1.0")  # type: ignore[arg-type]
