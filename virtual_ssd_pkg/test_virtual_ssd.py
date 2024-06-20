import os
import subprocess
from unittest import TestCase

from constants import INVALID_COMMAND, SSD_FILE_PATH, RESULT_FILE_PATH, NAND_FILE_PATH
from ssd import VirtualSSD
from file_io import FileIO

line_len = 11
FAKE_DATA = ('0x12345678')

class TestVirtualSSD(TestCase):
    def setUp(self):
        self.virtual_ssd = VirtualSSD()

    def test_cli_invalid_command(self):
        result = subprocess.run(['python', SSD_FILE_PATH, 'A'], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)

    def test_read_with_cli(self):
        subprocess.run(['python', SSD_FILE_PATH, 'W', '1', '0x00000000'])
        result = subprocess.run(['python', SSD_FILE_PATH, 'R', '1'], capture_output=True, text=True)
        self.assertIn('', result.stdout)
        file_io = FileIO(RESULT_FILE_PATH)
        ret = file_io.load()
        self.assertEqual(ret, '0x00000000')

    def test_read_with_cli_invalid_lba_range(self):
        result = subprocess.run(['python', SSD_FILE_PATH, 'R', '-1'], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)

        result = subprocess.run(['python', SSD_FILE_PATH, 'R', '100'], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)

    def test_write_with_cli(self):
        FAKE_LBA = 1
        result = subprocess.run(['python', SSD_FILE_PATH, 'W', str(FAKE_LBA), FAKE_DATA], capture_output=True, text=True)
        self.assertIn('', result.stdout)
        file_io = FileIO(NAND_FILE_PATH)
        ret = file_io.load()
        expected = ret[FAKE_LBA * line_len:(FAKE_LBA + 1) * line_len - 1]
        self.assertEqual(expected, FAKE_DATA)

    def test_write_with_cli_invalid_lba_range(self):
        FAKE_LBA = -1
        result = subprocess.run(['python', SSD_FILE_PATH, 'W', str(FAKE_LBA), FAKE_DATA], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)

        FAKE_LBA = 100
        result = subprocess.run(['python', SSD_FILE_PATH, 'W', str(FAKE_LBA), FAKE_DATA], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)

    def test_write_with_cli_invalid_data_range(self):
        FAKE_LBA = 1

        FAKE_DATA = '0000000000'
        result = subprocess.run(['python', SSD_FILE_PATH, 'W', str(FAKE_LBA), FAKE_DATA], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)

        FAKE_DATA = '0x0000000G'
        result = subprocess.run(['python', SSD_FILE_PATH, 'W', str(FAKE_LBA), FAKE_DATA], capture_output=True, text=True)
        self.assertIn(INVALID_COMMAND, result.stdout)
