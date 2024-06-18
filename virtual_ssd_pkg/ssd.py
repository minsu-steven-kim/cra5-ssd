from .file_io import FileIO


import sys


class VirtualSSD:
    def __init__(self):
        self.nand_file = 'nand.txt'
        self.result_file = 'result.txt'
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
        if value.startswith('0x') and len(value) == 10:
            return True
        return False

    def read(self, lba):
        self.valid_LBA(lba)

        nand_file_data = ['0x00000000' for _ in range(100)]
        nand_file_io = FileIO(self.nand_file)
        nand_file_data_raw = nand_file_io.load().strip().split('\n')

        for i, line in enumerate(nand_file_data_raw):
            nand_file_data[i] = line

        with open(self.result_file, 'w') as f:
            f.write(nand_file_data[int(lba)])


if __name__ == '__main__':
    ssd = VirtualSSD()
