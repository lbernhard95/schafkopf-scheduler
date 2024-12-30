from unittest.mock import patch

import pytest

from schafkopf.core import gmail


@pytest.fixture(autouse=True, scope='function')
def mock_gmail_send():
    with patch.object(gmail, "send") as mock_send:
        yield mock_send
