import os

from schafkopf.core import env


class TestReadOnly:
    def test_not_available(self):
        del os.environ["READ_ONLY"]
        assert env.read_only() is False

    def test_is_disabled(self):
        os.environ["READ_ONLY"] = "0"
        assert env.read_only() is False

    def test_is_enabled(self):
        os.environ["READ_ONLY"] = "1"
        assert env.read_only() is True
