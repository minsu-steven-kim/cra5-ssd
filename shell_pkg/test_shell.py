import os.path
from unittest import TestCase
from unittest.mock import Mock, patch
from shell_pkg.shell import Shell
import io
import sys

NON_INIT_VALUE = 0xAAAABBBB


class TestShell(TestCase):
    def setUp(self):
        self.vs = Shell()
        self.test_write_lba = 10
        self.test_write_value = NON_INIT_VALUE

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

    @patch.object(Shell, 'send_cmd_to_ssd')
    def test_read_calling_send_cmd_to_ssd(self,mock):
        self.vs.read(3)
        self.assertEqual(self.vs.send_cmd_to_ssd.call_count, 1)

    @patch.object(Shell, 'get_result_with_ssd')
    def test_read_calling_get_result_with_ssd(self):
        self.vs.get_result_with_ssd = Mock()
        self.vs.read(3)
        self.assertEqual(self.vs.get_result_with_ssd.call_count, 1)

    @patch.object(Shell, 'get_result_with_ssd', return_value =NON_INIT_VALUE)
    def test_read_check_print_result(self):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        try:
            self.vs.get_result_with_ssd = Mock()
            self.vs.get_result_with_ssd.return_value = NON_INIT_VALUE
            self.vs.read(3)
        finally:
            sys.stdout = original_stdout

        captured_output = int(output.getvalue().strip())
        self.assertEqual(captured_output, NON_INIT_VALUE)

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


    def test_read_check_invalid_lba(self):
        lba = 100
        with self.assertRaises(Exception) as context:
            self.vs.read(lba)
        self.assertEqual("INVALID COMMAND", str(context.exception))

