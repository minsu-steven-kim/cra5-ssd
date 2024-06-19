from unittest import TestCase
from virtual_ssd_pkg.command import WriteCommand, ReadCommand
from unittest.mock import mock_open, patch

FAKE_DATA = '0x12345678'
line_len = 11


class TestWriteCommand(TestCase):
    def setUp(self):
        self.command = WriteCommand()

    def test_write_command_invalid_text(self):
        args = ['ssd', 'W', '14234', '4']

        with self.assertRaises(Exception):
            self.command.execute(args)

    def test_write_command_invalid_lba(self):
        args = ['W', '14234', '0x00000000']

        with self.assertRaises(Exception):
            self.command.execute(args)

    def test_write_command_invalid_data(self):
        args = ['W', '1', '0000000000']

        with self.assertRaises(Exception):
            self.command.execute(args)

    def test_write_command_LBA_0(self):
        FAKE_LBA = 0
        args = ['W', str(FAKE_LBA), FAKE_DATA]
        self.command.execute(args)
        expected = self.command.NAND_TXT.load()[FAKE_LBA * line_len:(FAKE_LBA + 1) * line_len - 1]
        self.assertEqual(expected, FAKE_DATA)

    def test_write_command_LBA_1(self):
        FAKE_LBA = 1
        args = ['W', str(FAKE_LBA), FAKE_DATA]
        self.command.execute(args)
        expected = self.command.NAND_TXT.load()[FAKE_LBA * line_len:(FAKE_LBA + 1) * line_len - 1]
        self.assertEqual(expected, FAKE_DATA)

    def test_write_command_LBA_2(self):
        FAKE_LBA = 2
        args = ['W', str(FAKE_LBA), FAKE_DATA]
        self.command.execute(args)
        expected = self.command.NAND_TXT.load()[FAKE_LBA * line_len:(FAKE_LBA + 1) * line_len - 1]
        self.assertEqual(expected, FAKE_DATA)

    def test_write_command_LBA_50(self):
        FAKE_LBA = 50
        args = ['W', str(FAKE_LBA), FAKE_DATA]
        self.command.execute(args)
        expected = self.command.NAND_TXT.load()[FAKE_LBA * line_len:(FAKE_LBA + 1) * line_len - 1]
        self.assertEqual(expected, FAKE_DATA)


class TestReadCommand(TestCase):
    def setUp(self):
        self.executor = ReadCommand()

    @patch('builtins.open', new_callable=mock_open, read_data='0x00000000\n0x11111111\n0x22222222\n')
    def test_execute_with_mocked_file(self, mock_file):
        self.executor.execute([None, '1'])
        mock_file.assert_any_call('nand.txt', 'r')
        mock_file.assert_any_call('result.txt', 'w')

    def test_execute_lba_not_int_type(self):
        with self.assertRaises(Exception) as context:
            self.executor.execute([None, 'T'])

    def test_execute_lba_not_string_int_type(self):
        with self.assertRaises(Exception) as context:
            self.executor.execute([None, 1])

    def test_execute_lba_out_of_range(self):
        with self.assertRaises(Exception) as context:
            self.executor.execute([None, '-1'])

        with self.assertRaises(Exception) as context:
            self.executor.execute([None, '100'])
