import os
from shell_pkg.commands.command import Command
from shell_pkg.constants import INVALID_COMMAND, SSD_FILE_PATH


class WriteCommand(Command):
    def __init__(self, args):
        if len(args) != 3:
            raise Exception(INVALID_COMMAND)
        self.__lba = args[1]
        self.__value = args[2]
        self.__file_path = SSD_FILE_PATH

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
