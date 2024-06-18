import io
import sys
from unittest import TestCase
from unittest.mock import Mock

from shell_pkg.shell import Shell


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_read_calling_send_cmd_to_ssd(self):
        self.shell.send_cmd_to_ssd = Mock()
        self.shell.read(3)
        self.assertEqual(self.shell.send_cmd_to_ssd.call_count, 1)

    def test_read_calling_get_result_with_ssd(self):
        self.shell.get_result_with_ssd = Mock()
        self.shell.read(3)
        self.assertEqual(self.shell.get_result_with_ssd.call_count, 1)

    def test_read_check_print_result(self):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        try:
            self.shell.get_result_with_ssd = Mock()
            self.shell.get_result_with_ssd.return_value = 0xAAAABBBB
            self.shell.read(3)
        finally:
            sys.stdout = original_stdout

        captured_output = int(output.getvalue().strip())
        self.assertEqual(captured_output, 0xAAAABBBB)