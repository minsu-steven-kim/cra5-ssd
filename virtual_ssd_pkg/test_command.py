from unittest import TestCase

from virtual_ssd_pkg.command import WriteCommand

FAKE_DATA = '0xBAADEEEE'
line_len = 11

class TestCommand(TestCase):
    def setUp(self):
        self.command = WriteCommand()

    def test_write_command_invalid_text(self):
        args = 'ssd W 14234 4'

        with self.assertRaises(Exception):
            self.command.execute(args)

    def test_write_command_invalid_lba(self):
        args = 'ssd W 14234 0x00000000'

        with self.assertRaises(Exception):
            self.command.execute(args)
