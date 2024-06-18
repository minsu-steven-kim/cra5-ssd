from virtual_ssd_pkg.file_io import FileIO


import sys
import re

class VirtualSSD:
    def __init__(self):
        self.command = self.take_command()

    def take_command(self):
        try:
            arguments = ['ssd'] + sys.argv[1:]
            return self.parsing_command(' '.join(arguments))
        except ValueError:
            print('INVALID COMMAND')
        return None

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


if __name__ == '__main__':
    ssd = VirtualSSD()
