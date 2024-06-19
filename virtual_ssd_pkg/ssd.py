import sys

from command import InvalidCommand, WriteCommand, ReadCommand

INVALID_COMMAND = "INVALID COMMAND"


class VirtualSSD:
    def __init__(self):
        for filename in ['result.txt','nand.txt']:
            file = open(filename,'w')
            file.write("")

    def run(self):
        args = sys.argv[1:]
        cmd = self.determine_cmd(args)
        cmd.execute(args)

    def determine_cmd(self, args):
        if len(args) == 0:
            return InvalidCommand()
        elif args[0] == 'W':
            return WriteCommand()
        elif args[0] == 'R':
            return ReadCommand()
        else:
            return InvalidCommand()


if __name__ == '__main__':
    ssd = VirtualSSD()
    try:
        ssd.run()
    except Exception:
        print(INVALID_COMMAND)
