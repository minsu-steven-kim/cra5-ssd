from unittest import TestCase

from virtual_ssd_pkg.file_io import FileIO, ARRAY_SIZE

TARGET_LBA = 10
FAKE_DATA = 0x12345678
FAKE_DATA_SMALLEST = 0x00000000
FAKE_DATA_BIGGEST = 0xFFFFFFFF


class TestFileIO(TestCase):
    def setUp(self):
        super().setUp()
        self.io = FileIO()

    def test_initialize(self):
        self.assertIsNotNone(self.io.array)
        self.assertEqual(ARRAY_SIZE, len(self.io.array))

    def test_write_then_read(self):
        self.io.write(TARGET_LBA, FAKE_DATA)
        self.assertEqual(FAKE_DATA, self.io.read(TARGET_LBA))

    def test_write_then_read_smallest(self):
        self.io.write(TARGET_LBA, FAKE_DATA_SMALLEST)
        self.assertEqual(FAKE_DATA_SMALLEST, self.io.read(TARGET_LBA))

    def test_write_then_read_biggest(self):
        self.io.write(TARGET_LBA, FAKE_DATA_BIGGEST)
        self.assertEqual(FAKE_DATA_BIGGEST, self.io.read(TARGET_LBA))
