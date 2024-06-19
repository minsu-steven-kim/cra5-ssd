import os.path
from unittest import TestCase
from unittest.mock import Mock, patch

from command import WriteCommand, HelpCommand, ReadCommand, FullWriteCommand
from shell import Shell

import io
import sys

INVALID_LBA = "100"
VALID_LBA = "3"
TEST_SSD_FILE_PATH = "../virtual_ssd_pkg/ssd.py"
NON_INIT_VALUE = 0xAAAABBBB

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

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value = NON_INIT_VALUE)
    @patch.object(ReadCommand, 'send_cmd_to_ssd')
    def test_read_calling_send_cmd_to_ssd(self,sendMock, resMock):
        read = ReadCommand("../virtual_ssd_pkg/ssd.py", VALID_LBA)
        read.execute()
        self.assertEqual(read.send_cmd_to_ssd.call_count, 1)

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value = NON_INIT_VALUE)
    def test_read_calling_get_result_with_ssd(self, resMock):
        read = ReadCommand("../virtual_ssd_pkg/ssd.py", VALID_LBA)
        read.execute()
        self.assertEqual(read.get_result_with_ssd.call_count, 1)

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value =NON_INIT_VALUE)
    def test_read_check_print_result(self, resMock):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        try:
            read = ReadCommand("../virtual_ssd_pkg/ssd.py", VALID_LBA)
            read.execute()
        finally:
            sys.stdout = original_stdout

        captured_output = int(output.getvalue().strip())
        self.assertEqual(captured_output, NON_INIT_VALUE)

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

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value=NON_INIT_VALUE)
    def test_read_check_invalid_lba(self,resMock):
        lba = INVALID_LBA
        with self.assertRaises(Exception) as context:
            read = ReadCommand("../virtual_ssd_pkg/ssd.py", lba)
            read.execute()
        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_read_check_no_file(self):
        with self.assertRaises(FileNotFoundError):
            read = ReadCommand("../virtual_ssd_pkg/ssd.py", VALID_LBA)
            read.execute()

    def test_read_create_command(self):
        read = ReadCommand(TEST_SSD_FILE_PATH, VALID_LBA)
        actual = read.create_command()
        expected = f"python ../virtual_ssd_pkg/ssd.py ssd R 3"
        self.assertEqual(actual, expected)

    def test_fullwrite_invalid_range_value(self):
        with self.assertRaises(Exception) as context:
            wc = FullWriteCommand("0xAAAABBB")
            wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_fullwrite_invalid_type_value(self):
        with self.assertRaises(Exception) as context:
            wc = FullWriteCommand(0XFFFFFFFF)
            wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

