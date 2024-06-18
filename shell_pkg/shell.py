import os


class Shell:
    def __init__(self):
        pass

    def write(self, lba: int, value: str):
        if self.is_invalid_lba(lba):
            raise Exception("INVALID COMMAND")

    def is_invalid_lba(self, lba):
        if type(lba) != int:
            return True
        if lba < 0 or lba > 99:
            return True
        return False
