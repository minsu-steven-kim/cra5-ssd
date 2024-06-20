import sys

from command import CommandFactory
from constants import INVALID_COMMAND

import os
import sys
current_dir = os.path.dirname(__file__)
ROOT_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(ROOT_dir)
from logger_pkg.logger import Logger

class VirtualSSD:
    def __init__(self):
        self.command_factory = CommandFactory()

    def run(self):
        args = sys.argv[1:]
        cmd = self.command_factory.create_command(args)
        cmd.execute(args)

if __name__ == '__main__':
    ssd = VirtualSSD()
    try:
        ssd.run()
    except Exception:
        Logger().print(INVALID_COMMAND)
