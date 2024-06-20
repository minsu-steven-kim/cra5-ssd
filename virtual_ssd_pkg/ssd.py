import sys
from command import CommandFactory
from constants import INVALID_COMMAND

from constants import ROOT_PATH
sys.path.append(ROOT_PATH)
from logger_pkg.logger import Logger

class VirtualSSD:
    def __init__(self):
        self.command_factory = CommandFactory()

    def run(self):
        args = sys.argv[1:]
        cmd = self.command_factory.create_command(args)
        cmd.execute()

if __name__ == '__main__':
    ssd = VirtualSSD()
    try:
        ssd.run()
    except Exception:
        Logger().print(INVALID_COMMAND)
