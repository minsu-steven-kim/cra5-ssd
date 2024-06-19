from abc import ABC, abstractmethod
import re
import os

from constants import SSD_FILE_PATH, RESULT_FILE_PATH, INVALID_COMMAND, HELP_MESSAGE, \
    MIN_LBA, MAX_LBA


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    def is_invalid_lba(self, lba: str):
        if type(lba) != str:
            return True
        if not lba.isdigit():
            return True
        if MIN_LBA > int(lba) or int(lba) > MAX_LBA:
            return True
        return False

    def run_command(self, cmd):
        os.system(cmd)

    def is_invalid_value(self, value: str):
        if type(value) != str:
            return True
        return not bool(re.match(r'^0x[0-9A-F]{8}$', value))


class ExitCommand(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)
    def execute(self):
        return 1


class HelpCommand(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)
    def execute(self):
        print(HELP_MESSAGE)
        return 0


class InvalidCommand(Command):
    def execute(self):
        print(INVALID_COMMAND)
        return 0


class WriteCommand(Command):
    def __init__(self, args):
        if len(args) != 3:
            raise Exception(INVALID_COMMAND)
        self.__lba = args[1]
        self.__value = args[2]
        self.__file_path = SSD_FILE_PATH

    def get_lba(self):
        return self.__lba

    def set_lba(self, lba):
        self.__lba = lba

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def get_file_path(self):
        return self.__file_path

    def set_file_path(self, file_path):
        self.__file_path = file_path

    def execute(self):
        if self.is_invalid_parameter():
            raise Exception(INVALID_COMMAND)
        if not os.path.exists(self.__file_path):
            raise FileExistsError("VIRTUAL_SSD_PATH_ERROR")

        cmd = self.get_write_cmd_line()
        self.run_command(cmd)

    def is_invalid_parameter(self):
        if self.is_invalid_lba(self.__lba):
            return True
        if self.is_invalid_value(self.__value):
            return True
        return False

    def get_write_cmd_line(self):
        return f"python {self.__file_path} W {self.__lba} {self.__value}"


class ReadCommand(Command):
    def __init__(self, args):
        if not self.check_command_length(args):
            raise Exception(INVALID_COMMAND)
        self.lba = args[1]
        self.ssd_filepath = SSD_FILE_PATH
        self.result_filepath = RESULT_FILE_PATH

    def check_command_length(self, args):
        if len(args) == 2:
            return True
        return False

    def execute(self):
        if self.is_invalid_lba(self.lba):
            raise Exception(INVALID_COMMAND)
        if not os.path.exists(self.ssd_filepath):
            raise FileExistsError("VIRTUAL_SSD_PATH_ERROR")
        self.send_cmd_to_ssd()
        print(self.get_result_with_ssd())

    def get_result_with_ssd(self):
        with open(self.result_filepath, 'r') as f:
            return f.read()

    def create_command(self):
        return f"python {self.ssd_filepath} R {self.lba}"

    def send_cmd_to_ssd(self):
        cmd = self.create_command()
        self.run_command(cmd)


class FullwriteCommand(Command):
    def __init__(self, args):
        if len(args) != 2:
            raise Exception(INVALID_COMMAND)
        self.__value = args[1]
        self.__filepath = SSD_FILE_PATH

    def execute(self):
        if self.is_invalid_value(self.__value):
            raise Exception(INVALID_COMMAND)

        for lba in range(MAX_LBA + 1):
            WriteCommand(['write', str(lba), self.__value]).execute()


class FullreadCommand(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)

    def execute(self):
        for lba in range(MAX_LBA + 1):
            read_cmd = ReadCommand(['read', str(lba)])
            read_cmd.execute()


class TestApp1Command(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)
        self.testValue = '0xABCDFFFF'
        self.validationValue = '0xABCDFFFF\n' * (MAX_LBA + 1)

    def execute(self):
        fullWrite = FullwriteCommand(['fullwrite', self.testValue])
        fullWrite.execute()
        fullRead = FullreadCommand(['fullread'])
        fullRead.execute()


class TestApp2Command(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)

    def write_test1(self):
        args_list = [['write', str(i), '0xAAAABBBB'] for i in range(6)]
        for args in args_list:
            write_command = WriteCommand(args)
            for i in range(30):
                write_command.execute()

    def write_test2(self):
        args_list = [['write', str(i), '0x12345678'] for i in range(6)]
        for args in args_list:
            write_command = WriteCommand(args)
            write_command.execute()

    def read_test(self):
        args_list = [['read', str(i)] for i in range(6)]
        for args in args_list:
            read_command = ReadCommand(args)
            read_command.execute()

    def execute(self):
        self.write_test1()
        self.write_test2()
        self.read_test()
