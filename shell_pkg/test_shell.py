from unittest import TestCase
from unittest.mock import Mock

from shell_pkg.shell import Shell


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_placeholder(self):
        self.assertEqual(1, 1)

    def test_read_calling_send_cmd_to_ssd(self):
        self.shell.send_cmd_to_ssd = Mock()
        self.shell.read(3)
        self.assertEqual(self.shell.send_cmd_to_ssd.call_count, 1)

    def test_read_calling_get_result_with_ssd(self):
        self.shell.get_result_with_ssd = Mock()
        self.shell.read(3)
        self.assertEqual(self.shell.get_result_with_ssd.call_count, 1)