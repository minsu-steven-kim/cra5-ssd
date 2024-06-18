import os


class Shell:
    def __init__(self):
        pass

    def write(self, lba: int, value: int):
        if self.is_invalid_lba(lba):
            raise Exception("INVALID COMMAND")
        if self.is_invalid_value(value):
            raise Exception("INVALID COMMAND")

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
