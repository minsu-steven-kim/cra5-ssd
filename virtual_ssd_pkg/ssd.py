from file_io import FileIO
from command import InvalidCommand, WriteCommand, ReadCommand

import sys
import re


class VirtualSSD:
    def __init__(self):
        self.nand_file = 'nand.txt'
        self.result_file = 'result.txt'

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

    def parsing_command(self, cmd):
        if type(cmd) != str:
            raise ValueError("INVALID COMMAND")

        cmd_list = cmd.split(' ')
        if self.is_valid_read_command(cmd_list):
            return "READ"
        elif self.is_valid_write_command(cmd_list):
            return "WRITE"
        else:
            raise ValueError("INVALID COMMAND")

    def is_valid_write_command(self, cmd_list):
        return len(cmd_list) == 4 and cmd_list[0:2] == ['ssd', 'W'] and \
            self.valid_LBA(cmd_list[2]) and self.valid_value(cmd_list[3])

    def is_valid_read_command(self, cmd_list):
        return len(cmd_list) == 3 and cmd_list[0:2] == ['ssd', 'R'] and \
            self.valid_LBA(cmd_list[2])

    def valid_LBA(self, LBA):
        if LBA.isdigit():
            if 0 <= int(LBA) and int(LBA) <= 99:
                return True
        return False

    def valid_value(self, value):
        pattern = r'0x[0-9A-F]{8}$'
        return bool(re.match(pattern, value))

    def ssd_write(self, lba, data):
        if (not self.valid_LBA(lba)) or (not self.valid_value(data)):
            return

        self.NAND_TXT = FileIO("nand.txt")
        self.NAND_DATA = self.NAND_TXT.load()
        lba = int(lba)
        self.NAND_DATA = self.NAND_DATA[:lba * 11] + data + self.NAND_DATA[(lba + 1) * 11 - 1:]
        self.NAND_TXT.save(self.NAND_DATA)

    def read(self, lba):
        if not self.valid_LBA(lba):
            return

        nand_file_data = ['0x00000000' for _ in range(100)]
        nand_file_io = FileIO(self.nand_file)
        nand_file_data_raw = nand_file_io.load().strip().split('\n')

        for i, line in enumerate(nand_file_data_raw):
            nand_file_data[i] = line

        with open(self.result_file, 'w') as f:
            f.write(nand_file_data[int(lba)])


if __name__ == '__main__':
    ssd = VirtualSSD()
