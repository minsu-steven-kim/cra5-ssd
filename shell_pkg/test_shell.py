import os.path
from unittest import TestCase
from unittest.mock import Mock, patch
from shell_pkg.shell import Shell
from shell_pkg.command import HelpCommand
import io
import sys


class TestShell(TestCase):
    def setUp(self):
        self.vs = Shell()
        self.test_write_lba = 10
        self.test_write_value = 0xAAAABBBB

    def test_write_temporary(self):
        self.vs.write(1, 0x12341234)

    def test_write_invalid_lba(self):
        with self.assertRaises(Exception) as context:
            self.vs.write(100, 0x12341234)

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_type_lab(self):
        with self.assertRaises(Exception) as context:
            self.vs.write("10", 0x12341234)

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_range_value(self):
        with self.assertRaises(Exception) as context:
            self.vs.write(10, 0XFFFFFFFFF)

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_type_value(self):
        with self.assertRaises(Exception) as context:
            self.vs.write(10, "0XFFFFFFFF")

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_invalid_virtual_ssd_file_path(self):
        self.vs.set_virtual_ssd_file_path("123.py")
        with self.assertRaises(FileExistsError) as context:
            self.vs.write(10, 0XFFFFFFFF)

    def test_read_calling_send_cmd_to_ssd(self):
        self.vs.send_cmd_to_ssd = Mock()
        self.vs.read(3)
        self.assertEqual(self.vs.send_cmd_to_ssd.call_count, 1)

    def test_read_calling_get_result_with_ssd(self):
        self.vs.get_result_with_ssd = Mock()
        self.vs.read(3)
        self.assertEqual(self.vs.get_result_with_ssd.call_count, 1)

    def test_read_check_print_result(self):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        try:
            self.vs.get_result_with_ssd = Mock()
            self.vs.get_result_with_ssd.return_value = 0xAAAABBBB
            self.vs.read(3)
        finally:
            sys.stdout = original_stdout

        captured_output = int(output.getvalue().strip())
        self.assertEqual(captured_output, 0xAAAABBBB)

    @patch.object(Shell, "call_virtual_ssd_write_cmd")
    def test_check_call_write_cmd(self, mock):
        mock = Shell()
        mock.write(self.test_write_lba, self.test_write_value)

        self.assertEqual(1, mock.call_virtual_ssd_write_cmd.call_count, 1)
        mock.call_virtual_ssd_write_cmd.assert_called_with(self.test_write_lba, self.test_write_value)

    def test_check_write_cmd_line(self):
        result = self.vs.get_write_cmd_line(self.test_write_lba, self.test_write_value)
        answer = f"python {self.vs.get_virtual_ssd_file_path()} ssd W {self.test_write_lba} {self.test_write_value}"

        self.assertEqual(result, answer)

    @patch.object(Shell, "run_command")
    def test_check_call_write_cmd(self, mock):
        mock = Shell()
        mock.write(self.test_write_lba, self.test_write_value)
        cmd = mock.get_write_cmd_line(self.test_write_lba, self.test_write_value)

        mock.run_command.assert_called_with(cmd)
        self.assertEqual(1, mock.run_command.call_count)

    def test_print_help_command(self):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output

        try:
            HelpCommand().execute()
        finally:
            sys.stdout = original_stdout

        captured_output = output.getvalue()
        expected_output = """============================== Command Guide ==============================
1) write [LBA] [value]
: write [value] to [LBA].
: [LBA] should be an integer between 0 and 99.
: [value] should be in hexadecimal format between 0x00000000 and 0xFFFFFFFF.
2) read [LBA]
: read the value written to [LBA].
3) fullwrite [value]
: write [value] to all LBA(0~99).
: [value] should be in hexadecimal format between 0x00000000 and 0xFFFFFFFF.
4) fullread
: read the all LBA(0~99) values.
5) exit
: quit the shell.
6) help
: see the command guide.
"""
        self.assertEqual(expected_output, captured_output)