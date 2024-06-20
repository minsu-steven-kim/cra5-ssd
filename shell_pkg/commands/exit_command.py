from shell_pkg.commands.command import Command
from shell_pkg.constants import INVALID_COMMAND


class ExitCommand(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)

    def execute(self):
        return 1
