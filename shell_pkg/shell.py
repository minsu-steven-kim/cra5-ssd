from command import InvalidCommand, ExitCommand, HelpCommand, WriteCommand, ReadCommand, EraseCommand, \
    EraseRangeCommand, FullreadCommand, \
    FullwriteCommand, TestApp1Command, TestApp2Command

import os
import sys
current_dir = os.path.dirname(__file__)
ROOT_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(ROOT_dir)
from logger_pkg.logger import Logger

class Shell:
    def run(self):
        is_exit = 0
        while not is_exit:
            try:
                print('> ', end='')
                args = input().split()
                cmd = self.determine_cmd(args)
                is_exit = cmd.execute()
            except Exception as e:
                Logger().print(e)

    def determine_cmd(self, args):
        if len(args) == 0:
            return InvalidCommand()
        elif args[0] == 'exit':
            return ExitCommand(args)
        elif args[0] == 'help':
            return HelpCommand(args)
        elif args[0] == 'write':
            return WriteCommand(args)
        elif args[0] == 'read':
            return ReadCommand(args)
        elif args[0] == 'erase':
            return EraseCommand(args)
        elif args[0] == 'erase_range':
            return EraseRangeCommand(args)
        elif args[0] == 'fullwrite':
            return FullwriteCommand(args)
        elif args[0] == 'fullread':
            return FullreadCommand(args)
        elif args[0] == 'testapp1':
            return TestApp1Command(args)
        elif args[0] == 'testapp2':
            return TestApp2Command(args)
        else:
            return InvalidCommand()


if __name__ == '__main__':
    shell = Shell()
    shell.run()
