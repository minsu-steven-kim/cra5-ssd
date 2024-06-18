import os

class Shell:
    def __init__(self):
        pass

    def write(self, lba: int, value: str):
        if type(lba) != int:
            raise Exception("INVALID COMMAND")
        if lba < 0 or lba > 99:
            raise Exception("INVALID COMMAND")
