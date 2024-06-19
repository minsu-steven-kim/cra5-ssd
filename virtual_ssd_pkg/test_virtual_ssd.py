import os
from unittest import TestCase
from unittest.mock import patch

from virtual_ssd_pkg.ssd import VirtualSSD


class TestVirtualSSD(TestCase):
    def setUp(self):
        self.virtual_ssd = VirtualSSD()

    @patch('os.system')
    def test_cli_invalid_command(self, mock_system):
        mock_system.return_value = 1
        result = os.system('python ssd.py A')
        self.assertEqual(result, 1)

    @patch('os.system')
    def test_read_with_cli(self, mock_system):
        mock_system.return_value = 0
        result = os.system('python ssd.py R 1')
        self.assertEqual(result, 0)

    @patch('os.system')
    def test_read_with_cli_invalid_lba_range(self, mock_system):
        mock_system.return_value = 1
        result = os.system('python ssd.py R -1')
        self.assertEqual(result, 1)

        result = os.system('python ssd.py R 100')
        self.assertEqual(result, 1)

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
