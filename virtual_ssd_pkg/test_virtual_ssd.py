from unittest import TestCase
from unittest.mock import mock_open, patch

from virtual_ssd_pkg.ssd import VirtualSSD

FAKE_DATA = '0xBAADEEEE'
line_len = 11


class TestVirtualSSD(TestCase):
    def setUp(self):
        self.virtual_ssd = VirtualSSD()

    def test_placeholder(self):
        self.assertEqual(1, 1)

    def test_command_not_string(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command(123)

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_read_command_invalid_string(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd R 1234 123")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_write_command_invalid_string(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd W 1234")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_read_LBA_not_int_type(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd R AAA")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_read_LBA_out_of_range(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd R 1234")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_read_called(self):
        self.assertEqual("READ", self.virtual_ssd.parsing_command("ssd R 10"))

    def test_write_LBA_not_int_type(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd W AAA")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_write_LBA_out_of_range(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd W 1234")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_write_invalue_value_not_started_0x(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd W 10 1234")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_write_invalid_value_length(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd W 10 0x1234")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_write_invalid_value_length2(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd W 10 0xFFFFFFFFFF")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_write_called(self):
        self.assertEqual("WRITE", self.virtual_ssd.parsing_command("ssd W 10 0x10000000"))

    def test_write_called2(self):
        self.assertEqual("WRITE", self.virtual_ssd.parsing_command("ssd W 10 0x1AAAFFFF"))

    def test_write_invalid_value(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd W 10 0x0000000H")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_write_invalid_value_lower(self):
        with self.assertRaises(ValueError) as context:
            self.virtual_ssd.parsing_command("ssd W 10 0x1234567f")

        self.assertEqual(str(context.exception), "INVALID COMMAND")

    def test_write_LBA_0(self):
        FAKE_LBA = '0'
        self.virtual_ssd.ssd_write(FAKE_LBA, FAKE_DATA)
        FAKE_LBA = int(FAKE_LBA)
        expected = self.virtual_ssd.NAND_TXT.load()[FAKE_LBA * line_len:(FAKE_LBA + 1) * line_len - 1]
        self.assertEqual(expected, FAKE_DATA)

    def test_write_LBA_1(self):
        FAKE_LBA = '1'
        self.virtual_ssd.ssd_write(FAKE_LBA, FAKE_DATA)
        FAKE_LBA = int(FAKE_LBA)
        expected = self.virtual_ssd.NAND_TXT.load()[FAKE_LBA * line_len:(FAKE_LBA + 1) * line_len - 1]
        self.assertEqual(expected, FAKE_DATA)

    def test_write_LBA_2(self):
        FAKE_LBA = '2'
        self.virtual_ssd.ssd_write(FAKE_LBA, FAKE_DATA)
        FAKE_LBA = int(FAKE_LBA)
        expected = self.virtual_ssd.NAND_TXT.load()[FAKE_LBA * line_len:(FAKE_LBA + 1) * line_len - 1]
        self.assertEqual(expected, FAKE_DATA)

    def test_write_LBA_50(self):
        FAKE_LBA = '50'
        self.virtual_ssd.ssd_write(FAKE_LBA, FAKE_DATA)
        FAKE_LBA = int(FAKE_LBA)
        expected = self.virtual_ssd.NAND_TXT.load()[FAKE_LBA * line_len:(FAKE_LBA + 1) * line_len - 1]
        self.assertEqual(expected, FAKE_DATA)
