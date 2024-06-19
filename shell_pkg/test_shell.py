import os.path
from unittest import TestCase
from unittest.mock import Mock, patch

from command import WriteCommand
from shell import Shell
import io
import sys


class TestShell(TestCase):
    def setUp(self):
        self.vs = Shell()
        self.wc = WriteCommand("../virtual_ssd_pkg/ssd.py", 10, 0xAAAABBBB)

    def test_write_execute_invalid_lba(self):
        with self.assertRaises(Exception) as context:
            wc = WriteCommand("../virtual_ssd_pkg/ssd.py", "100", "0xAAAABBBB")
            wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_type_lab(self):
        with self.assertRaises(Exception) as context:
            wc = WriteCommand("../virtual_ssd_pkg/ssd.py", 10, "0xAAAABBBB")
            wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_range_value(self):
        with self.assertRaises(Exception) as context:
            wc = WriteCommand("../virtual_ssd_pkg/ssd.py", "10", "0xAAAABBB")
            wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_type_value(self):
        with self.assertRaises(Exception) as context:
            wc = WriteCommand("../virtual_ssd_pkg/ssd.py", "10", 0XFFFFFFFF)
            wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_invalid_virtual_ssd_file_path(self):
        with self.assertRaises(FileExistsError) as context:
            wc = WriteCommand("123.py", "10", "0xFFFFFFFF")
            wc.execute()

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
