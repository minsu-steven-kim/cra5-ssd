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
