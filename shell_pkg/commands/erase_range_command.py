import os
from shell_pkg.commands.erase_command import EraseCommand, Command
from shell_pkg.constants import INVALID_COMMAND, SSD_FILE_PATH, MAX_SIZE_PER_COMMAND, MAX_LBA, MAX_NUM_LBA


class EraseRangeCommand(Command):
    def __init__(self, args):
        if len(args) != 3:
            raise Exception(INVALID_COMMAND)
        self.__start_lba = args[1]
        self.__end_lba = args[2]
        self.__file_path = SSD_FILE_PATH

    def is_invalid_end_lba(self, start_lba: str, end_lba: str):
        if int(start_lba) > int(end_lba):
            return True
        return False

    def generate_commands(self):
        commands = []
        size = int(self.__end_lba) - int(self.__start_lba)
        lba = int(self.__start_lba)

        while size > 0:
            current_size = min(size, MAX_SIZE_PER_COMMAND)

            if lba > MAX_LBA:
                break

            if lba + current_size > MAX_NUM_LBA:
                current_size = MAX_NUM_LBA - lba

            commands.append([str(lba), str(current_size)])
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
            EraseCommand(['erase', command[0], command[1]]).execute()

    def is_invalid_parameter(self):
        if self.is_invalid_lba(self.__start_lba):
            return True
        if self.is_invalid_lba(self.__end_lba):
            return True
        if self.is_invalid_end_lba(self.__start_lba, self.__end_lba):
            return True
        return False
