from shell_pkg.commands.command import Command
from shell_pkg.constants import INVALID_COMMAND


class InvalidCommand(Command):
    def execute(self):
        self.print(INVALID_COMMAND)
        return 0
