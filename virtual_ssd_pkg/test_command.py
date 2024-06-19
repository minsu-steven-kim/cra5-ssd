from unittest import TestCase
from unittest.mock import mock_open, patch

from virtual_ssd_pkg.command import ReadCommand


class TestReadCommand(TestCase):
    def setUp(self):
        self.executor = ReadCommand()

    @patch('builtins.open', new_callable=mock_open, read_data='0x00000000\n0x11111111\n0x22222222\n')
    def test_execute_with_mocked_file(self, mock_file):
        self.executor.execute([None, '1'])
        mock_file.assert_any_call('nand.txt', 'r')
        mock_file.assert_any_call('result.txt', 'w')

    def test_execute_lba_not_int_type(self):
        with self.assertRaises(ValueError) as context:
            self.executor.execute([None, 'T'])

    def test_execute_lba_not_string_int_type(self):
        with self.assertRaises(ValueError) as context:
            self.executor.execute([None, 1])

    def test_execute_lba_out_of_range(self):
        with self.assertRaises(ValueError) as context:
            self.executor.execute([None, '-1'])

        with self.assertRaises(ValueError) as context:
            self.executor.execute([None, '100'])
