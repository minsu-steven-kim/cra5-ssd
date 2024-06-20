import sys
from command import CommandFactory
from constants import INVALID_COMMAND
from buffer_manager import BufferManager

from constants import ROOT_PATH
sys.path.append(ROOT_PATH)
from logger_pkg.logger import Logger

class VirtualSSD:
    def __init__(self):
        self.bm = BufferManager()
        self.command_factory = CommandFactory()

    def run(self):
        args = sys.argv[1:]
        cmd = self.command_factory.create_command(args)
        self.bm.run(args)
        # TO-DO: ReadCommand 및 FlushCommand 만 BufferManager 거치지 않도록 수정 필요
        # cmd.execute(args)


if __name__ == '__main__':
    ssd = VirtualSSD()
    try:
        ssd.run()
    except Exception as e:
        Logger().print(e)
