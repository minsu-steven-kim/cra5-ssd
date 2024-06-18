from abc import ABC, abstractmethod


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
    def execute(self):
        self.send_cmd_to_ssd()
        print(self.get_result_with_ssd())