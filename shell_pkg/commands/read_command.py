import os
from shell_pkg.commands.command import Command
from shell_pkg.constants import INVALID_COMMAND, SSD_FILE_PATH, RESULT_FILE_PATH


class ReadCommand(Command):
    def __init__(self, args):
        if not self.check_command_length(args):
            raise Exception(INVALID_COMMAND)
        self.lba = args[1]
        self.ssd_filepath = SSD_FILE_PATH
        self.result_filepath = RESULT_FILE_PATH

    def check_command_length(self, args):
        if len(args) == 2:
            return True
        return False

    def execute(self):
        if self.is_invalid_lba(self.lba):
            raise Exception(INVALID_COMMAND)
        if not os.path.exists(self.ssd_filepath):
            raise FileExistsError("VIRTUAL_SSD_PATH_ERROR")
        self.send_cmd_to_ssd()
        self.print(self.get_result_with_ssd())

    def get_result_with_ssd(self):
        with open(self.result_filepath, 'r') as f:
            return f.read()

    def create_command(self):
        return f"python {self.ssd_filepath} R {self.lba}"

    def send_cmd_to_ssd(self):
        cmd = self.create_command()
        print(cmd)
        self.run_command(cmd)
