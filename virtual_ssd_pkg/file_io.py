class FileIO:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ''

    def save(self, data):
        with open(self.filename, 'w') as f:
            f.write(data)
