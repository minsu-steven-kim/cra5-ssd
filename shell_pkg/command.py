from abc import ABC, abstractmethod
import re
import os


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    def is_invalid_lba(self, lba: str):
        if type(lba) != str:
            return True
        if not lba.isdigit():
            return True
        if 0 > int(lba) or int(lba) > 99:
            return True
        return False

    def run_command(self, cmd):
        os.system(cmd)

    def is_invalid_value(self, value: str):
        if type(value) != str:
            return True
        return not bool(re.match(r'0x[0-9A-F]{8}$', value))


class ExitCommand(Command):
    def execute(self):
        return 1

class HelpCommand(Command):
    def execute(self):
        print("""============================== Command Guide ==============================
1) write [LBA] [value]
: write [value] to [LBA].
: [LBA] should be an integer between 0 and 99.
: [value] should be in hexadecimal format between 0x00000000 and 0xFFFFFFFF.
2) read [LBA]
: read the value written to [LBA].
3) fullwrite [value]
: write [value] to all LBA(0~99).
: [value] should be in hexadecimal format between 0x00000000 and 0xFFFFFFFF.
4) fullread
: read the all LBA(0~99) values.
5) exit
: quit the shell.
6) help
: see the command guide.""")
        return 0


class InvalidCommand(Command):
    def execute(self):
        print('INVALID COMMAND')
        return 0


class WriteCommand(Command):
    def __init__(self, file_path, args):
        if len(args) != 3:
            raise Exception("INVALID COMMAND")
        self.__lba = args[1]
        self.__value = args[2]
        self.__file_path = file_path

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
            raise Exception("INVALID COMMAND")
        if not os.path.exists(self.__file_path):
            raise FileExistsError("VIRTUAL_FILE_PATH_ERROR")

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
    def __init__(self, filepath, args):
        if not self.check_command_length(args):
            raise Exception("INVALID COMMAND")
        self.lba = args[1]
        self.filepath = filepath

    def check_command_length(self, args):
        if len(args) == 2:
            return True
        return False

    def execute(self):
        if self.is_invalid_lba(self.lba):
            raise Exception("INVALID COMMAND")
        if not os.path.exists(self.filepath):
            raise FileExistsError("VIRTUAL_FILE_PATH_ERROR")
        self.send_cmd_to_ssd()
        print(self.get_result_with_ssd())

    def get_result_with_ssd(self):
        with open('result.txt', 'r') as f:
            return f.read()

    def create_command(self):
        return f"python {self.filepath} R {self.lba}"

    def send_cmd_to_ssd(self):
        cmd = self.create_command()
        self.run_command(cmd)

class FullwriteCommand(Command):
    def __init__(self, filepath, args):
        if len(args) != 2:
            raise Exception("INVALID COMMAND")
        self.filepath = filepath
        self.__value = args[1]

    def execute(self):
        if self.is_invalid_value(self.__value):
            raise Exception("INVALID COMMAND")

        for lba in range(100):
            WriteCommand(self.filepath, ['write', str(lba), self.__value]).execute()

class FullreadCommand(Command):
    def __init__(self, filepath):
        self.filepath = filepath

    def execute(self):
        for lba in range(100):
            read_cmd = ReadCommand(self.filepath, ['read', str(lba)])
            read_cmd.execute()

class TestApp1Command(Command):
    def __init__(self, filepath):
        self.filepath = filepath
        self.testValue = '0xABCDFFFF'
        self.validationValue = '0xABCDFFFF\n' * 100

    def execute(self):
        fullWrite = FullwriteCommand(self.filepath, ['fullwrite', self.testValue])
        fullWrite.execute()
        fullRead = FullreadCommand(self.filepath)
        fullRead.execute()

class TestApp2Command(Command):
    def __init__(self, filepath):
        self.filepath = filepath

    def write_test1(self):
        args_list = [[None, str(i), '0xAAAABBBB'] for i in range(6)]
        for args in args_list:
            write_command = WriteCommand(self.filepath, args)
            for i in range(30):
                write_command.execute()

    def write_test2(self):
        args_list = [[None, str(i), '0x12345678'] for i in range(6)]
        for args in args_list:
            write_command = WriteCommand(self.filepath, args)
            write_command.execute()

    def read_test(self):
        args_list = [[None, str(i)] for i in range(6)]
        for args in args_list:
            read_command = ReadCommand(self.filepath, args)
            read_command.execute()

    def execute(self):
        self.write_test1()
        self.write_test2()
        self.read_test()
