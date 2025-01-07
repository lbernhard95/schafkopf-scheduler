import os

from schafkopf.core import env


class TestReadOnly:
    def test_not_available(self):
        del os.environ["READ_ONLY"]
        assert env.read_only() is False

    def test_is_disabled(self):
        os.environ["READ_ONLY"] = "false"
        assert env.read_only() is False

    def test_is_enabled(self):
        os.environ["READ_ONLY"] = "true"
        assert env.read_only() is True