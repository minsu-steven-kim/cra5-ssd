import os
from command import InvalidCommand, ExitCommand, HelpCommand, WriteCommand, ReadCommand, FullreadCommand


class Shell:
    def __init__(self):
        self.__virtual_ssd_file_path = "../virtual_ssd_pkg/ssd.py"

    def run(self):
        is_exit = 0
        while not is_exit:
            print('> ', end='')
            args = input().split()
            cmd = self.determine_cmd(args)
            is_exit = cmd.execute()

    def determine_cmd(self, args):
        if len(args) == 0:
            return InvalidCommand()
        elif args[0] == 'exit':
            return ExitCommand()
        elif args[0] == 'help':
            return HelpCommand()
        elif args[0] == 'write':
            return WriteCommand(self.__virtual_ssd_file_path, args)
        elif args[0] == 'read':
            return ReadCommand(self.__virtual_ssd_file_path, args[1])
        elif args[0] == 'fullread':
            return FullreadCommand(self.__virtual_ssd_file_path)
        else:
            return InvalidCommand()

    def set_virtual_ssd_file_path(self, file_path):
        self.__virtual_ssd_file_path = file_path

    def get_virtual_ssd_file_path(self):
        return self.__virtual_ssd_file_path

if __name__ == '__main__':
    shell = Shell()
    shell.run()
