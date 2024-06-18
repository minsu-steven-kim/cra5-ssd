INITIAL_VALUE = 0
ARRAY_SIZE = 100
NAND_FILENAME = f'{__file__}/../nand.txt'


class FileIO:
    def __init__(self):
        self.array = [INITIAL_VALUE for _ in range(ARRAY_SIZE)]
        self.load()

    def load(self):
        try:
            with open(NAND_FILENAME, 'rt') as f:
                for i, line in enumerate(f.readlines()):
                    self.array[i] = int(line.strip(), 16)
        except FileNotFoundError:
            pass

    def save(self):
        with open(NAND_FILENAME, 'wt') as f:
            for value in self.array:
                f.write(format(value, '08x'))
                f.write('\n')

    def read(self, lba):
        return self.array[lba]

    def write(self, lba, data):
        self.array[lba] = data
        self.save()


if __name__ == '__main__':
    io = FileIO()
    io.load()
    print(io.array)
    io.write(10, 0x12345678)
    io.save()
    io.load()
    print(io.array)
    io.write(10, 0xFFFFFFFF)
    io.save()
    io.load()
    print(io.array)
