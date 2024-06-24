from shell_pkg.commands.write_command import WriteCommand, Command
from shell_pkg.constants import INVALID_COMMAND, SSD_FILE_PATH, MAX_LBA


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
