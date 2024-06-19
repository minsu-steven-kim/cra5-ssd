import os.path
from unittest import TestCase
from unittest.mock import Mock, patch

from command import WriteCommand, HelpCommand, ReadCommand, FullwriteCommand, FullreadCommand
from shell import Shell

import io
import sys

INVALID_LBA = "100"
INVALID_TYPE_LBA = 10
VALID_LBA = "3"
VALID_VALUE = "0xAAAABBBB"
INVALID_RANGE_VALUE = "0xAAABBB"
TEST_SSD_FILE_PATH = "../virtual_ssd_pkg/ssd.py"
NON_INIT_VALUE = 0xAAAABBBB


class TestShell(TestCase):
    def setUp(self):
        self.vs = Shell()
        self.wc = WriteCommand(TEST_SSD_FILE_PATH, ["write", VALID_LBA, VALID_VALUE])
        self.read_cmd_valid_lba = ['read', VALID_LBA]
        self.read_cmd_invalid_lba = ['read', INVALID_LBA]

    def test_write_execute_invalid_lba(self):
        with self.assertRaises(Exception) as context:
            self.wc.set_lba(INVALID_LBA)
            self.wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_type_lab(self):
        with self.assertRaises(Exception) as context:
            self.wc.set_lba(INVALID_TYPE_LBA)
            self.wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_range_value(self):
        with self.assertRaises(Exception) as context:
            self.wc.set_value(INVALID_RANGE_VALUE)
            self.wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_type_value(self):
        with self.assertRaises(Exception) as context:
            self.wc.set_value(NON_INIT_VALUE)
            self.wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_invalid_virtual_ssd_file_path(self):
        with self.assertRaises(FileExistsError) as context:
            self.wc.set_file_path("123.py")
            self.wc.execute()

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value=NON_INIT_VALUE)
    @patch.object(ReadCommand, 'send_cmd_to_ssd')
    def test_read_calling_send_cmd_to_ssd(self, sendMock, resMock):
        read = ReadCommand("../virtual_ssd_pkg/ssd.py", self.read_cmd_valid_lba)
        read.execute()
        self.assertEqual(read.send_cmd_to_ssd.call_count, 1)

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value=NON_INIT_VALUE)
    def test_read_calling_get_result_with_ssd(self, resMock):
        read = ReadCommand("../virtual_ssd_pkg/ssd.py", self.read_cmd_valid_lba)
        read.execute()
        self.assertEqual(read.get_result_with_ssd.call_count, 1)

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

    def test_check_write_cmd_line(self):
        cmd = f"python {self.vs.get_virtual_ssd_file_path()} W {self.wc.get_lba()} {self.wc.get_value()}"

        self.assertEqual(self.wc.get_write_cmd_line(), cmd)

    @patch.object(WriteCommand, "run_command")
    def test_check_call_write_cmd(self, mock):
        mock = WriteCommand(TEST_SSD_FILE_PATH, ["write", VALID_LBA, VALID_VALUE])
        mock.execute()
        cmd = mock.get_write_cmd_line()

        self.assertEqual(1, mock.run_command.call_count)
        mock.run_command.assert_called_with(cmd)

    def test_init_write_command_without_value(self):
        with self.assertRaises(Exception) as context:
            wc = WriteCommand(TEST_SSD_FILE_PATH, ["write", VALID_LBA])

        self.assertEqual("INVALID COMMAND", str(context.exception))

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value=NON_INIT_VALUE)
    def test_read_check_invalid_lba(self, resMock):
        lba = INVALID_LBA
        with self.assertRaises(Exception) as context:
            read = ReadCommand(TEST_SSD_FILE_PATH, lba)
            read.execute()
        self.assertEqual("INVALID COMMAND", str(context.exception))

    @patch.object(ReadCommand, 'send_cmd_to_ssd')
    def test_read_check_no_file(self, sendMock):
        if os.path.exists('result.txt'):
            os.remove('result.txt')
        with self.assertRaises(FileNotFoundError):
            read = ReadCommand(TEST_SSD_FILE_PATH, self.read_cmd_valid_lba)
            read.execute()

    def test_read_create_command(self):
        read = ReadCommand(TEST_SSD_FILE_PATH, self.read_cmd_valid_lba)
        actual = read.create_command()
        expected = f"python ../virtual_ssd_pkg/ssd.py R 3"
        self.assertEqual(actual, expected)

    def test_fullwrite_invalid_range_value(self):
        with self.assertRaises(Exception) as context:
            wc = FullwriteCommand(TEST_SSD_FILE_PATH, ["fullwrite", INVALID_RANGE_VALUE])
            wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_fullwrite_invalid_type_value(self):
        with self.assertRaises(Exception) as context:
            wc = FullwriteCommand(TEST_SSD_FILE_PATH, ["fullwrite", NON_INIT_VALUE])
            wc.execute()

        self.assertEqual("INVALID COMMAND", str(context.exception))

    @patch.object(WriteCommand, 'execute')
    def test_fullwirte_with_mocked_write_commands(self, mock_execute):
        fullwrite_command = FullwriteCommand(TEST_SSD_FILE_PATH, ["fullwrite", VALID_VALUE])
        fullwrite_command.execute()
        self.assertEqual(mock_execute.call_count, 100)

    @patch.object(ReadCommand, 'execute')
    def test_fullread_with_mocked_read_commands(self, mock_execute):
        fullread_command = FullreadCommand(TEST_SSD_FILE_PATH)
        fullread_command.execute()
        self.assertEqual(mock_execute.call_count, 100)
