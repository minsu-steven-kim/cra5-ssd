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

    def is_invalid_value(self, value: str):
        if type(value) != str:
            return True
        return not bool(re.match(r'0x[0-9A-F]{8}$', value))

    def run_command(self, cmd):
        os.system(cmd)


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
    def __init__(self, file_path, lba: int, value: str):
        self.lba = lba
        self.value = value
        self.file_path = file_path

    def execute(self):
        if self.is_invalid_parameter():
            raise Exception("INVALID COMMAND")
        if not os.path.exists(self.file_path):
            raise FileExistsError("VIRTUAL_FILE_PATH_ERROR")

        cmd = self.get_write_cmd_line()
        self.run_command(cmd)

    def set_write_cmd_line(self, lba, value):
        self.cmd = f"python {self.__virtual_ssd_file_path} ssd W {lba} {value}"

    def is_invalid_parameter(self):
        if self.is_invalid_lba(self.lba):
            return True
        if self.is_invalid_value(self.value):
            return True
        return False

    def get_write_cmd_line(self):
        return f"python {self.file_path} W {self.lba} {self.value}"
