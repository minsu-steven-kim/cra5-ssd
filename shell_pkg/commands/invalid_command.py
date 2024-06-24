from shell_pkg.commands.command import Command
from shell_pkg.constants import INVALID_COMMAND


class InvalidCommand(Command):
    def execute(self):
        return 0
