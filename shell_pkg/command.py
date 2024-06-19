from abc import ABC, abstractmethod
import os

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class ExitCommand(Command):
    def execute(self):
        return 1


class InvalidCommand(Command):
    def execute(self):
        print('INVALID COMMAND')
        return 0

class ReadCommand(Command):
    def __init__(self, filepath, lba):
        self.lba = lba
        self.filepath = filepath
    def execute(self):
        if self.is_invalid_lba(self.lba):
            raise Exception("INVALID COMMAND")
        self.send_cmd_to_ssd()
        print(self.get_result_with_ssd())
    def get_result_with_ssd(self):
        with open('result.txt', 'r') as f:
            return f.read()
    def create_command(self):
        return f"python {self.filepath} ssd R {self.lba}"

    def run_command(self, cmd):
        os.system(cmd)

    def send_cmd_to_ssd(self):
        cmd = self.create_command()
        self.run_command(cmd)

    def is_invalid_lba(self, lba):
        if type(lba) != int:
            return True
        if lba < 0 or lba > 99:
            return True
        return False