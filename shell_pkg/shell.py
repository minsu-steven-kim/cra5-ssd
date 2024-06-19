import os
from command import InvalidCommand, ExitCommand, HelpCommand, WriteCommand


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
        elif args[0] == 'write' and len(args) == 3:
            return WriteCommand(self.__virtual_ssd_file_path, args[1], args[2])
        else:
            return InvalidCommand()

    def set_virtual_ssd_file_path(self, file_path):
        self.__virtual_ssd_file_path = file_path

    def get_virtual_ssd_file_path(self):
        return self.__virtual_ssd_file_path

    def read(self, param):
        self.send_cmd_to_ssd()
        print(self.get_result_with_ssd())

    def send_cmd_to_ssd(self):
        pass

    def get_result_with_ssd(self):
        pass


if __name__ == '__main__':
    shell = Shell()
    shell.run()
