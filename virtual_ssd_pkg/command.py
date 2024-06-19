from abc import ABC, abstractmethod
import re
import os
from file_io import FileIO


class Command(ABC):
    def __init__(self):
        self.nand_file = 'nand.txt'
        self.result_file = 'result.txt'

    @abstractmethod
    def execute(self, args):
        pass

    def is_invalid_lba(self, lba: str):
        if type(lba) != str:
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
    def execute(self, args):
        pass


class ReadCommand(Command):
    def execute(self, args):
        if self.is_invalid_lba(args[1]):
            raise ValueError("INVALID COMMAND")

        nand_file_data = ['0x00000000' for _ in range(100)]
        nand_file_io = FileIO(self.nand_file)
        nand_file_data_raw = nand_file_io.load().strip().split('\n')

        for i, line in enumerate(nand_file_data_raw):
            nand_file_data[i] = line

        result_file_io = FileIO(self.result_file)
        result_file_io.save(nand_file_data[int(args[1])])


class InvalidCommand(Command):

    def execute(self, args):
        print('INVALID COMMAND')
