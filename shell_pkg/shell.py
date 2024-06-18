import os

from command import InvalidCommand, ExitCommand


class Shell:
    def __init__(self):
        self.__virtual_ssd_file_path = "../virtual_ssd_pkg/ssd.py"

    def run(self):
        is_exit = 0
        while not is_exit:
            print('> ', end='')
            args = input().split()
            cmd = self.determine_cmd(args)
            is_exit = cmd.execute()

    def determine_cmd(self, args):
        if len(args) == 0:
            return InvalidCommand()
        elif args[0] == 'exit':
            return ExitCommand()
        else:
            return InvalidCommand()

    def get_virtual_ssd_file_path(self):
        return self.__virtual_ssd_file_path

    def set_virtual_ssd_file_path(self, file_path):
        self.__virtual_ssd_file_path = file_path

    def write(self, lba: int, value: int):
        if self.is_valid_parameter(lba, value):
            raise Exception("INVALID COMMAND")
        if not os.path.exists(self.__virtual_ssd_file_path):
            raise FileExistsError("VIRTUAL_FILE_PATH_ERROR")

    def is_valid_parameter(self, lba, value):
        if self.is_invalid_lba(lba):
            return True
        if self.is_invalid_value(value):
            return True
        return False

    def is_invalid_lba(self, lba):
        if type(lba) != int:
            return True
        if lba < 0 or lba > 99:
            return True
        return False

    def is_invalid_value(self, value):
        if type(value) != int:
            return True
        if value < 0x00000000 or value > 0xFFFFFFFF:
            return True
        return False

    def read(self, param):
        self.send_cmd_to_ssd()
        print(self.get_result_with_ssd())

    def send_cmd_to_ssd(self):
        pass

    def get_result_with_ssd(self):
        pass


if __name__ == '__main__':
    shell = Shell()
    shell.run()
