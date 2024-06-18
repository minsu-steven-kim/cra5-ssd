import os


class Shell:
    def __init__(self):
        self.__virtual_ssd_file_path = "../virtual_ssd_pkg/virtual_ssd.py"

    def get_virtual_ssd_file_path(self):
        return self.__virtual_ssd_file_path

    def set_virtual_ssd_file_path(self, file_path):
        self.__virtual_ssd_file_path = file_path

    def write(self, lba: int, value: int):
        if self.is_invalid_lba(lba):
            raise Exception("INVALID COMMAND")
        if self.is_invalid_value(value):
            raise Exception("INVALID COMMAND")

        if not os.path.exists(self.__virtual_ssd_file_path):
            raise FileExistsError("VIRTUAL_FILE_PATH_ERROR")

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
