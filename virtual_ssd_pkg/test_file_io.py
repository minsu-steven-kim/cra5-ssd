from unittest import TestCase
from virtual_ssd_pkg.file_io import FileIO


class TestFileIO(TestCase):
    def setUp(self):
        super().setUp()
        self.io = FileIO('virtual_ssd_pkg/nand.txt')

    def test_initialize(self):
        self.assertEqual('virtual_ssd_pkg/nand.txt', self.io.filename)
