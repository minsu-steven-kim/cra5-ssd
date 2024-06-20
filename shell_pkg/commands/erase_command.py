import os
from shell_pkg.commands.command import Command
from shell_pkg.constants import INVALID_COMMAND, SSD_FILE_PATH, MAX_ERASE_SIZE, MIN_ERASE_SIZE, MAX_SIZE_PER_COMMAND, MAX_LBA, MAX_NUM_LBA


class EraseCommand(Command):
    def __init__(self, args):
        if len(args) != 3:
            raise Exception(INVALID_COMMAND)
        self.__lba = args[1]
        self.__size = args[2]
        self.__file_path = SSD_FILE_PATH

    def is_invalid_size(self, size: str):
        if type(size) != str:
            return True
        if not size.isdigit():
            return True
        if MIN_ERASE_SIZE > int(size) or MAX_ERASE_SIZE < int(size):
            return True
        return False

    def generate_commands(self):
        commands = []
        size = int(self.__size)
        lba = int(self.__lba)

        while size > 0:
            current_size = min(size, MAX_SIZE_PER_COMMAND)

            if lba > MAX_LBA:
                break
            if lba + current_size > MAX_NUM_LBA:
                current_size = MAX_NUM_LBA - lba

            commands.append(self.get_erase_cmd_line(str(lba), str(current_size)))
            lba += current_size
            size -= current_size

        return commands

    def execute(self):
        if self.is_invalid_parameter():
            raise Exception(INVALID_COMMAND)
        if not os.path.exists(self.__file_path):
            raise FileExistsError("VIRTUAL_SSD_PATH_ERROR")

        commands = self.generate_commands()

        for command in commands:
            self.run_command(command)

    def is_invalid_parameter(self):
        if self.is_invalid_lba(self.__lba):
            return True
        if self.is_invalid_size(self.__size):
            return True
        return False

    def get_erase_cmd_line(self, lba, size):
        return f"python {self.__file_path} E {lba} {size}"
