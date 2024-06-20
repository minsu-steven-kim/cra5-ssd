import sys

from command import CommandFactory
from constants import INVALID_COMMAND
from virtual_ssd_pkg.buffer_manager import BufferManager


class VirtualSSD:
    def __init__(self):
        self.bm = BufferManager()
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
        print(INVALID_COMMAND)
