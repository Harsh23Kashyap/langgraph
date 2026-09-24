def default_retry_on(exc: Exception) -> bool:
    try:
        import httpx
    except ImportError:
        httpx = None  # type: ignore[assignment]
    try:
        import requests
    except ImportError:
        requests = None  # type: ignore[assignment]

    if isinstance(exc, ConnectionError):
        return True
    # Match the `requests.HTTPError` branch below: guard against a manually
    # raised `HTTPStatusError` with no `response` attached. (`httpx` always
    # sets `response` for its own client-side raises, but a user-raised
    # instance with `response=None` would crash here otherwise.)
    if httpx is not None and isinstance(exc, httpx.HTTPStatusError):
        if exc.response is None:
            return True
        return 500 <= exc.response.status_code < 600
    if requests is not None and isinstance(exc, requests.HTTPError):
        if exc.response is None:
            return True
        return 500 <= exc.response.status_code < 600
    if isinstance(
        exc,
        (
            ValueError,
            TypeError,
            ArithmeticError,
            ImportError,
            LookupError,
            NameError,
            SyntaxError,
            RuntimeError,
            ReferenceError,
            StopIteration,
            StopAsyncIteration,
            OSError,
        ),
    ):
        return False
    return True
