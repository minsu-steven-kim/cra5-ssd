from unittest import TestCase
from unittest.mock import Mock

from shell_pkg.shell import Shell


class TestShell(TestCase):
    def test_placeholder(self):
        self.assertEqual(1, 1)

    def test_read_calling_send_cmd_to_ssd(self):
        shell = Shell()
        shell.send_cmd_to_ssd = Mock()
        shell.read(3)
        self.assertEqual(shell.send_cmd_to_ssd.call_count, 1)