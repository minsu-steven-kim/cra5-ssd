from unittest import TestCase
from shell import Shell

class TestShell(TestCase):
    def test_placeholder(self):
        self.assertEqual(1, 1)

    def test_write_temporary(self):
        vs = Shell()
        vs.write(1, "ox12341234")
