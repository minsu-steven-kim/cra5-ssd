from shell_pkg.commands.read_command import ReadCommand, Command
from shell_pkg.constants import INVALID_COMMAND, MAX_LBA


class FullreadCommand(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)

    def execute(self):
        for lba in range(MAX_LBA + 1):
            read_cmd = ReadCommand(['read', str(lba)])
            read_cmd.execute()
