from shell_pkg.commands.command import Command
from shell_pkg.constants import INVALID_COMMAND, SSD_FILE_PATH


class FlushCommand(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)

    def execute(self):
        self.run_command(self.get_flush_cmd_line())

    def get_flush_cmd_line(self):
        return f"python {SSD_FILE_PATH} F"
