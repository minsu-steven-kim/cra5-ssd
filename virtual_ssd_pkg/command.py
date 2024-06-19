import re
from abc import ABC, abstractmethod

from constants import INVALID_COMMAND, NAND_FILE_PATH, RESULT_FILE_PATH, MIN_LBA, MAX_LBA
from file_io import FileIO


class Command(ABC):
    def __init__(self):
        self.nand_file = NAND_FILE_PATH
        self.result_file = RESULT_FILE_PATH

    @abstractmethod
    def execute(self, args):
        pass

    def is_invalid_lba(self, lba: str):
        if type(lba) != str:
            return True
        if len(lba) == 0:
            return True
        if not lba.isdigit():
            return True
        if  MIN_LBA > int(lba) or int(lba) > MAX_LBA:
            return True
        return False

    def is_invalid_value(self, value: str):
        if type(value) != str:
            return True
        return not bool(re.match(r'^0x[0-9A-F]{8}$', value))


class WriteCommand(Command):
    def is_invalid_parameter(self, args):
        if len(args) != 3:
            return True
        if self.is_invalid_lba(args[1]):
            return True
        if self.is_invalid_value(args[2]):
            return True
        return False

    def execute(self, args):
        if self.is_invalid_parameter(args):
            raise Exception(INVALID_COMMAND)
        self.NAND_TXT = FileIO(self.nand_file)
        self.NAND_DATA = self.NAND_TXT.load()
        lba = int(args[1])
        data = args[2]
        self.NAND_DATA = self.NAND_DATA[:lba * 11] + data + self.NAND_DATA[(lba + 1) * 11 - 1:]
        self.NAND_TXT.save(self.NAND_DATA)


class ReadCommand(Command):
    def execute(self, args):
        if len(args) != 2:
            raise Exception(INVALID_COMMAND)
        if self.is_invalid_lba(args[1]):
            raise Exception(INVALID_COMMAND)

        nand_file_data = ['0x00000000' for _ in range(MAX_LBA + 1)]
        nand_file_io = FileIO(self.nand_file)
        nand_file_data_raw = nand_file_io.load().strip().split('\n')

        for i, line in enumerate(nand_file_data_raw):
            nand_file_data[i] = line

        result_file_io = FileIO(self.result_file)
        result_file_io.save(nand_file_data[int(args[1])])


class InvalidCommand(Command):

    def execute(self, args):
        raise Exception(INVALID_COMMAND)
