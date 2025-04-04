import os
from unittest.mock import patch

import pytest

from core.gmail.client import GmailClient


@pytest.fixture(autouse=True, scope="function")
def mock_gmail_send():
    with patch.object(GmailClient, "send") as mock_send:
        yield mock_send


@pytest.fixture(autouse=True, scope="function")
def mock_environment():
    os.environ["READ_ONLY"] = "0"
    yield
