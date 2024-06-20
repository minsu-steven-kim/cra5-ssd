import re
from abc import ABC, abstractmethod

from constants import INVALID_COMMAND, NAND_FILE_PATH, RESULT_FILE_PATH, MIN_LBA, MAX_LBA, MIN_SIZE, MAX_SIZE, BUFFER_FILE_PATH
from file_io import FileIO


class CommandFactory:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = CommandFactory()
        return cls._instance

    @staticmethod
    def create_command(args):
        if len(args) == 0:
            return InvalidCommand()
        elif args[0] == 'W':
            return WriteCommand()
        elif args[0] == 'R':
            return ReadCommand()
        elif args[0] == 'E':
            return EraseCommand()
        elif args[0] == 'F':
            return FlushCommand()
        else:
            return InvalidCommand()


class Command(ABC):
    def __init__(self):
        self.command_factory = CommandFactory()
        self.nand_file = NAND_FILE_PATH
        self.result_file = RESULT_FILE_PATH
        self.buffer_file = BUFFER_FILE_PATH

    @abstractmethod
    def execute(self, args):
        pass


    @abstractmethod
    def is_invalid_parameter(self, args):
        pass

    
    @staticmethod
    def is_invalid_lba(lba: str):
        if type(lba) != str:
            return True
        if len(lba) == 0:
            return True
        if not lba.isdigit():
            return True
        if MIN_LBA > int(lba) or int(lba) > MAX_LBA:
            return True
        return False

    @staticmethod
    def is_invalid_value(value: str):
        if type(value) != str:
            return True
        return not bool(re.match(r'^0x[0-9A-F]{8}$', value))

    @staticmethod
    def is_invalid_size(self, size: str):
        if type(size) != str:
            return True
        if len(size) == 0:
            return True
        if not size.isdigit():
            return True
        if int(size) < MIN_SIZE or int(size) > MAX_SIZE:
            return True
        return False


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

    def is_invalid_parameter(self, args):
        if len(args) != 2:
            return True
        if self.is_invalid_lba(args[1]):
            return True
        return False

    def execute(self, args):
        if self.is_invalid_parameter(args):
            raise Exception(INVALID_COMMAND)
        nand_file_data = ['0x00000000' for _ in range(MAX_LBA + 1)]
        nand_file_io = FileIO(self.nand_file)
        nand_file_data_raw = nand_file_io.load().strip().split('\n')

        for i, line in enumerate(nand_file_data_raw):
            nand_file_data[i] = line

        result_file_io = FileIO(self.result_file)
        result_file_io.save(nand_file_data[int(args[1])])


class EraseCommand(Command):
    def is_invalid_parameter(self, args):
        if len(args) != 3:
            return True
        if self.is_invalid_lba(args[1]):
            return True
        if self.is_invalid_size(args[2]):
            return True
        return False
    def set_range(self, lba, size):
        self.start_location = int(lba)
        self.end_location = self.start_location + int(size)
        if self.end_location > MAX_LBA:
            self.end_location = MAX_LBA + 1

    def execute(self, args):
        if self.is_invalid_parameter(args):
            raise Exception(INVALID_COMMAND)
        self.set_range(args[1], args[2])

        self.NAND_TXT = FileIO(self.nand_file)
        self.NAND_DATA = self.NAND_TXT.load()

        for lba in range(self.start_location, self.end_location):
            loc = lba * 11
            self.NAND_DATA = self.NAND_DATA[:loc] + "0x00000000" + self.NAND_DATA[loc + 10:]
        self.NAND_TXT.save(self.NAND_DATA)


class InvalidCommand(Command):
    def execute(self, args):
        raise Exception(INVALID_COMMAND)


class FlushCommand(Command):
    def execute(self, args):
        buffer = FileIO(self.buffer_file)
        raw_string = buffer.load().strip()

        if len(raw_string) == 0:
            return

        command_strings = raw_string.split('\n')
        for command_string in command_strings:
            args = command_string.split()
            command = self.command_factory.create_command(args)
            command.execute(args)

        buffer.save('')
