from abc import ABC, abstractmethod
import re

from virtual_ssd_pkg.file_io import FileIO


class Command(ABC):
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
        if 0 > int(lba) or int(lba) > 99:
            return True
        return False

    def is_invalid_value(self, value: str):
        if type(value) != str:
            return True
        return not bool(re.match(r'0x[0-9A-F]{8}$', value))


class WriteCommand(Command):
    def __init__(self):
        pass

    def is_invalid_parameter(self, args):
        if len(args) < 3:
            return True
        if self.is_invalid_lba(args[1]):
            return True
        if self.is_invalid_value(args[2]):
            return True
        return False

    def execute(self, args):
        if self.is_invalid_parameter(args):
            raise Exception("INVALID COMMAND")
        self.NAND_TXT = FileIO("nand.txt")
        self.NAND_DATA = self.NAND_TXT.load()
        lba = int(args[1])
        data = args[2]
        self.NAND_DATA = self.NAND_DATA[:lba * 11] + data + self.NAND_DATA[(lba + 1) * 11 - 1:]
        self.NAND_TXT.save(self.NAND_DATA)


class ReadCommand(Command):
    def execute(self, args):
        pass


class InvalidCommand(Command):

    def execute(self, args):
        raise Exception("INVALID COMMAND")
