from constants import RESULT_FILE_PATH, BUFFER_FILE_PATH


class FileIO:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                if self.filename == RESULT_FILE_PATH:
                    return f.read()
                if self.filename == BUFFER_FILE_PATH:
                    return f.read()
                file_read = f.read()
                if len(file_read) != 1100:
                    f.close()
                    file_read = self.initial_read()
                return file_read
        except FileNotFoundError:
            if self.filename == BUFFER_FILE_PATH:
                return ''
            return self.initial_read()

    def save(self, data):
        with open(self.filename, 'w') as f:
            f.write(data)

    def initial_read(self):
        f = open(self.filename, 'w')
        for i in range(100):
            f.write("0x00000000\n")
        f.close()
        f = open(self.filename, 'r')
        return f.read()
