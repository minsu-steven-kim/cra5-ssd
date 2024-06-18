from unittest import TestCase
from virtual_ssd_pkg.file_io import FileIO

FAKE_FILENAME = 'virtual_ssd_pkg/nand.txt'


class TestFileIO(TestCase):
    def setUp(self):
        super().setUp()
        self.io = FileIO(FAKE_FILENAME)

    def test_initialize(self):
        self.assertEqual(FAKE_FILENAME, self.io.filename)
