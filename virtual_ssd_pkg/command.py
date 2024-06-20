import re
from abc import ABC, abstractmethod

from constants import INVALID_COMMAND, NAND_FILE_PATH, RESULT_FILE_PATH, MIN_LBA, MAX_LBA, MIN_SIZE, MAX_SIZE, \
    BUFFER_FILE_PATH
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
            return WriteCommand(args)
        elif args[0] == 'R':
            return ReadCommand(args)
        elif args[0] == 'E':
            return EraseCommand(args)
        elif args[0] == 'F':
            return FlushCommand(args)
        else:
            return InvalidCommand()


class Command(ABC):
    def __init__(self):
        self.command_factory = CommandFactory()
        self.nand_file = NAND_FILE_PATH
        self.result_file = RESULT_FILE_PATH
        self.buffer_file = BUFFER_FILE_PATH

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def validate(self):
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
    def is_invalid_size(size: str):
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
    def __init__(self, args):
        super().__init__()
        if len(args) != 3:
            raise Exception(INVALID_COMMAND)
        self.lba = args[1]
        self.value = args[2]
        self.validate()

    def validate(self):
        if self.is_invalid_lba(self.lba):
            raise Exception(INVALID_COMMAND)
        if self.is_invalid_value(self.value):
            raise Exception(INVALID_COMMAND)

    def execute(self):
        self.NAND_TXT = FileIO(self.nand_file)
        self.NAND_DATA = self.NAND_TXT.load()
        lba = int(self.lba)
        data = self.value
        self.NAND_DATA = self.NAND_DATA[:lba * 11] + data + self.NAND_DATA[(lba + 1) * 11 - 1:]
        self.NAND_TXT.save(self.NAND_DATA)


class ReadCommand(Command):
    def __init__(self, args):
        super().__init__()
        if len(args) != 2:
            raise Exception(INVALID_COMMAND)
        self.lba = args[1]
        self.validate()

    def validate(self):
        if self.is_invalid_lba(self.lba):
            raise Exception(INVALID_COMMAND)

    def execute(self):
        nand_file_data = ['0x00000000' for _ in range(MAX_LBA + 1)]
        nand_file_io = FileIO(self.nand_file)
        nand_file_data_raw = nand_file_io.load().strip().split('\n')

        for i, line in enumerate(nand_file_data_raw):
            nand_file_data[i] = line

        result_file_io = FileIO(self.result_file)
        result_file_io.save(nand_file_data[int(self.lba)])


class EraseCommand(Command):
    def __init__(self, args):
        super().__init__()
        if len(args) != 2:
            raise Exception(INVALID_COMMAND)
        self.lba = args[1]
        self.size = args[2]
        self.validate()

    def validate(self):
        if self.is_invalid_lba(self.lba):
            raise Exception(INVALID_COMMAND)
        if self.is_invalid_size(self.size):
            raise Exception(INVALID_COMMAND)

    def set_range(self):
        start_location = int(self.lba)
        end_location = start_location + int(self.size)
        if end_location > MAX_LBA:
            end_location = MAX_LBA + 1
        return start_location, end_location

    def execute(self):
        start_location, end_location = self.set_range()
        self.NAND_TXT = FileIO(self.nand_file)
        self.NAND_DATA = self.NAND_TXT.load()

        for lba in range(start_location, end_location):
            loc = lba * 11
            self.NAND_DATA = self.NAND_DATA[:loc] + "0x00000000" + self.NAND_DATA[loc + 10:]

        self.NAND_TXT.save(self.NAND_DATA)



class FlushCommand(Command):
    def __init__(self, args):
        super().__init__()
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)
        self.validate()

    def validate(self):
        pass

    def execute(self):
        buffer = FileIO(self.buffer_file)
        raw_string = buffer.load().strip()

        if len(raw_string) == 0:
            return

        command_strings = raw_string.split('\n')
        for command_string in command_strings:
            args = command_string.split()
            command = self.command_factory.create_command(args)
            command.execute()

        buffer.save('')


class InvalidCommand(Command):
    def validate(self):
        pass

    def execute(self):
        raise Exception(INVALID_COMMAND)
