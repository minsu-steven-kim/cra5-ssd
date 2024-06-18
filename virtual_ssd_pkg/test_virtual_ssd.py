from unittest import TestCase

from virtual_ssd import VirtualSSD

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



