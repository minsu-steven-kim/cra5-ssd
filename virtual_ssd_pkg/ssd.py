import sys

from buffer_manager import BufferManager
from command import CommandFactory, FlushCommand
from constants import ROOT_PATH

sys.path.append(ROOT_PATH)
from logger_pkg.logger import Logger


class VirtualSSD:
    def __init__(self):
        self.bm = BufferManager()
        self.command_factory = CommandFactory.get_instance()

    def run(self):
        args = sys.argv[1:]
        cmd = self.command_factory.create_command(args)

        if isinstance(cmd, FlushCommand):
            cmd.execute()
        else:
            self.bm.run(cmd)


if __name__ == '__main__':
    ssd = VirtualSSD()
    try:
        ssd.run()
    except Exception as e:
        Logger().print(str(e))
