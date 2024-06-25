import os.path
from unittest import TestCase
from unittest.mock import Mock, patch

import io
import sys

from constants import INVALID_COMMAND, SSD_FILE_PATH, RESULT_FILE_PATH, HELP_MESSAGE
from command import WriteCommand, HelpCommand, ReadCommand, FullwriteCommand, FullreadCommand, TestApp1Command, \
    TestApp2Command
from shell import Shell

INVALID_LBA = "100"
INVALID_TYPE_LBA = 10
VALID_LBA = "3"
TEST_SSD_FILE_PATH = SSD_FILE_PATH
TEST_RESULT_FILE_PATH = RESULT_FILE_PATH
VALID_VALUE = "0xAAAABBBB"
INVALID_RANGE_VALUE = "0xAAABBB"
NON_INIT_VALUE = 0xAAAABBBB


class TestShell(TestCase):
    def setUp(self):
        self.vs = Shell()
        self.wc = WriteCommand(["write", VALID_LBA, VALID_VALUE])
        self.read_cmd_valid_lba = ['read', VALID_LBA]
        self.read_cmd_invalid_lba = ['read', INVALID_LBA]

    def test_write_execute_invalid_lba(self):
        with self.assertRaises(Exception) as context:
            self.wc.set_lba(INVALID_LBA)
            self.wc.execute()

        self.assertEqual(INVALID_COMMAND, str(context.exception))

    def test_write_invalid_type_lba(self):
        with self.assertRaises(Exception) as context:
            self.wc.set_lba(INVALID_TYPE_LBA)
            self.wc.execute()

        self.assertEqual(INVALID_COMMAND, str(context.exception))

    def test_write_invalid_range_value(self):
        with self.assertRaises(Exception) as context:
            self.wc.set_value(INVALID_RANGE_VALUE)
            self.wc.execute()

        self.assertEqual(INVALID_COMMAND, str(context.exception))

    def test_write_invalid_type_value(self):
        with self.assertRaises(Exception) as context:
            self.wc.set_value(NON_INIT_VALUE)
            self.wc.execute()

        self.assertEqual(INVALID_COMMAND, str(context.exception))

    def test_invalid_virtual_ssd_file_path(self):
        with self.assertRaises(FileExistsError) as context:
            self.wc.set_file_path("123.py")
            self.wc.execute()

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value=NON_INIT_VALUE)
    @patch.object(ReadCommand, 'send_cmd_to_ssd')
    def test_read_calling_send_cmd_to_ssd(self, sendMock, resMock):
        read = ReadCommand(self.read_cmd_valid_lba)
        read.execute()
        self.assertEqual(read.send_cmd_to_ssd.call_count, 1)

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value=NON_INIT_VALUE)
    def test_read_calling_get_result_with_ssd(self, resMock):
        read = ReadCommand(self.read_cmd_valid_lba)
        read.execute()
        self.assertEqual(read.get_result_with_ssd.call_count, 1)

    def test_print_help_command(self):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output

        try:
            HelpCommand(['help']).execute()
        finally:
            sys.stdout = original_stdout

        captured_output = output.getvalue().strip()
        expected_output = HELP_MESSAGE.strip()
        self.assertEqual(expected_output, captured_output)

    def test_check_write_cmd_line(self):
        cmd = f"python {TEST_SSD_FILE_PATH} W {self.wc.get_lba()} {self.wc.get_value()}"

        self.assertEqual(self.wc.get_write_cmd_line(), cmd)

    @patch.object(WriteCommand, "run_command")
    def test_check_call_write_cmd(self, mock):
        mock = WriteCommand(["write", VALID_LBA, VALID_VALUE])
        mock.execute()
        cmd = mock.get_write_cmd_line()

        self.assertEqual(1, mock.run_command.call_count)
        mock.run_command.assert_called_with(cmd)

    def test_init_write_command_without_value(self):
        with self.assertRaises(Exception) as context:
            wc = WriteCommand(["write", VALID_LBA])

        self.assertEqual(INVALID_COMMAND, str(context.exception))

    @patch.object(ReadCommand, 'get_result_with_ssd', return_value=NON_INIT_VALUE)
    def test_read_check_invalid_lba(self, resMock):
        lba = INVALID_LBA
        with self.assertRaises(Exception) as context:
            read = ReadCommand(lba)
            read.execute()
        self.assertEqual(INVALID_COMMAND, str(context.exception))

    @patch.object(ReadCommand, 'send_cmd_to_ssd')
    def test_read_check_no_file(self, sendMock):
        if os.path.exists(TEST_RESULT_FILE_PATH):
            os.remove(TEST_RESULT_FILE_PATH)
        with self.assertRaises(FileNotFoundError):
            read = ReadCommand(self.read_cmd_valid_lba)
            read.execute()

    def test_read_create_command(self):
        read = ReadCommand(self.read_cmd_valid_lba)
        actual = read.create_command()
        expected = f"python {TEST_SSD_FILE_PATH} R 3"
        self.assertEqual(actual, expected)

    def test_fullwrite_invalid_range_value(self):
        with self.assertRaises(Exception) as context:
            wc = FullwriteCommand(["fullwrite", INVALID_RANGE_VALUE])
            wc.execute()

        self.assertEqual(INVALID_COMMAND, str(context.exception))

    def test_fullwrite_invalid_type_value(self):
        with self.assertRaises(Exception) as context:
            wc = FullwriteCommand(["fullwrite", NON_INIT_VALUE])
            wc.execute()

        self.assertEqual(INVALID_COMMAND, str(context.exception))

    @patch.object(WriteCommand, 'execute')
    def test_fullwrite_with_mocked_write_commands(self, mock_execute):
        fullwrite_command = FullwriteCommand(["fullwrite", VALID_VALUE])
        fullwrite_command.execute()
        self.assertEqual(mock_execute.call_count, 100)

    @patch.object(ReadCommand, 'execute')
    def test_fullread_with_mocked_read_commands(self, mock_execute):
        fullread_command = FullreadCommand(['fullread'])
        fullread_command.execute()
        self.assertEqual(mock_execute.call_count, 100)

    @patch.object(WriteCommand, 'execute')
    def test_app2_calling_write_command(self, mock_execute):
        testapp2 = TestApp2Command(['testapp2'])
        testapp2.execute()
        self.assertEqual(mock_execute.call_count, 186)

    @patch.object(ReadCommand, 'execute')
    def test_app2_calling_read_command(self, mock_execute):
        testapp2 = TestApp2Command(['testapp2'])
        testapp2.execute()
        self.assertEqual(mock_execute.call_count, 6)

    def test_app2_compare_value(self):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output

        try:
            testapp1 = TestApp2Command(['testapp2'])
            testapp1.execute()
        finally:
            sys.stdout = original_stdout

        captured_output = output.getvalue()
        expected = '0x12345678\n' * 6
        self.assertEqual(captured_output, expected)

    @patch.object(FullwriteCommand, 'execute')
    @patch.object(FullreadCommand, 'execute')
    def test_app1_calling_fullwrite_and_fullread(self, mock_fullread_execute, mock_fullwrite_execute):
        testapp1 = TestApp1Command(['testapp1'])
        testapp1.execute()
        self.assertEqual(mock_fullread_execute.call_count, 1)
        self.assertEqual(mock_fullwrite_execute.call_count, 1)

    def test_app1_compare_value(self):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output

        try:
            testapp1 = TestApp1Command(['testapp1'])
            testapp1.execute()
        finally:
            sys.stdout = original_stdout

        captured_output = output.getvalue()
        expected = '0xABCDFFFF\n' * 100
        self.assertEqual(captured_output, expected)

    @patch('builtins.input', side_effect=['write 1', 'exit'])
    def test_determine_cmd_with_wrong_cmd(self, mock):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output

        try:
            mock = Shell()
            mock.run()
        finally:
            sys.stdout = original_stdout

        self.assertIn(INVALID_COMMAND, output.getvalue())

    @patch('builtins.input', side_effect=['help', 'exit'])
    def test_determine_cmd_with_help(self, mock):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output

        try:
            mock = Shell()
            mock.run()
        finally:
            sys.stdout = original_stdout

        self.assertIn(HELP_MESSAGE, output.getvalue())
