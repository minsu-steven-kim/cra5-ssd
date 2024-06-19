import os
import subprocess
from unittest import TestCase
from unittest.mock import patch

from ssd import VirtualSSD
from file_io import FileIO

INVALID_COMMAND = "INVALID COMMAND"

class TestVirtualSSD(TestCase):
    def setUp(self):
        self.virtual_ssd = VirtualSSD()

    def test_cli_invalid_command(self):
        result = subprocess.run(['python', 'ssd.py', 'A'], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)

    def test_read_with_cli(self):
        result = subprocess.run(['python', 'ssd.py', 'R', '1'], capture_output=True, text=True)
        self.assertIn('', result.stdout)
        file_io = FileIO('result.txt')
        ret = file_io.load()
        self.assertEqual(ret, '0x00000000')

    def test_read_with_cli_invalid_lba_range(self):
        result = subprocess.run(['python', 'ssd.py', 'R', '-1'], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)

        result = subprocess.run(['python', 'ssd.py', 'R', '100'], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)

    @patch('os.system')
    def test_write_with_cli(self, mock_system):
        mock_system.return_value = 0
        result = os.system('python ssd.py W 1 0x00000000')
        self.assertEqual(result, 0)

    @patch('os.system')
    def test_write_with_cli_invalid_lba_range(self, mock_system):
        mock_system.return_value = 1
        result = os.system('python ssd.py W -1 0x00000000')
        self.assertEqual(result, 1)

        result = os.system('python ssd.py W 100 0x00000000')
        self.assertEqual(result, 1)

    @patch('os.system')
    def test_write_with_cli_invalid_data_range(self, mock_system):
        mock_system.return_value = 1
        result = os.system('python ssd.py W 0 0000000000')
        self.assertEqual(result, 1)

        result = os.system('python ssd.py W 0 0x0000000H')
        self.assertEqual(result, 1)
