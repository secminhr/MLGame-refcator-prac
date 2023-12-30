from contextlib import contextmanager
from unittest.mock import Mock


@contextmanager
def assert_same(mock_calls):
    expected_calls = Mock()
    try:
        yield expected_calls
    finally:
        assert mock_calls == expected_calls.mock_calls