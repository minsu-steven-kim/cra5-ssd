from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, args):
        pass


class WriteCommand(Command):
    def execute(self, args):
        pass


class ReadCommand(Command):
    def execute(self, args):
        pass


class InvalidCommand(Command):

    def execute(self, args):
        print('INVALID COMMAND')
