from unittest import TestCase
from shell import Shell


class TestShell(TestCase):
    def test_placeholder(self):
        self.assertEqual(1, 1)

    def test_write_temporary(self):
        vs = Shell()
        vs.write(1, 0x12341234)

    def test_write_invalid_lba(self):
        vs = Shell()
        with self.assertRaises(Exception) as context:
            vs.write(100, 0x12341234)

        self.assertEqual("INVALID COMMAND", str(context.exception))

    def test_write_invalid_type_lab(self):
        vs = Shell()
        with self.assertRaises(Exception) as context:
            vs.write("10", 0x12341234)

        self.assertEqual("INVALID COMMAND", str(context.exception))
