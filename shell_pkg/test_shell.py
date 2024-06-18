import io
import sys
from unittest import TestCase
from unittest.mock import Mock, patch

from shell_pkg.shell import Shell

NON_INIT_DATA = 0xAAAABBBB


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    @patch.object(Shell, 'send_cmd_to_ssd')
    def test_read_calling_send_cmd_to_ssd(self, mock):
        self.shell.read(3)
        self.assertEqual(self.shell.send_cmd_to_ssd.call_count, 1)

    @patch.object(Shell, 'get_result_with_ssd')
    def test_read_calling_get_result_with_ssd(self, mock):
        self.shell.get_result_with_ssd = Mock()
        self.shell.read(3)
        self.assertEqual(self.shell.get_result_with_ssd.call_count, 1)

    @patch.object(Shell, 'get_result_with_ssd', return_value = NON_INIT_DATA)
    def test_read_check_print_result(self, mock):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        try:
            self.shell.read(3)
        finally:
            sys.stdout = original_stdout

        captured_output = int(output.getvalue().strip())
        self.assertEqual(captured_output, NON_INIT_DATA)