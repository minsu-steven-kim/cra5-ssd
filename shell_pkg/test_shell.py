import os.path
from unittest import TestCase

from shell import Shell


class TestShell(TestCase):
    def setUp(self):
        self.vs = Shell()

    def test_write_temporary(self):
        self.vs.write(1, 0x12341234)

    def test_write_invalid_lba(self):
        with self.assertRaises(Exception) as context:
            self.vs.write(100, 0x12341234)

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_type_lab(self):
        with self.assertRaises(Exception) as context:
            self.vs.write("10", 0x12341234)

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_range_value(self):
        with self.assertRaises(Exception) as context:
            self.vs.write(10, 0XFFFFFFFFF)

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_type_value(self):
        with self.assertRaises(Exception) as context:
            self.vs.write(10, "0XFFFFFFFF")

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_invalid_virtual_ssd_file_path(self):
        self.vs.set_virtual_ssd_file_path("123.py")
        with self.assertRaises(FileExistsError) as context:
            self.vs.write(10, 0XFFFFFFFF)
