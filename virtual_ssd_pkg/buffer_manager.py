import os.path

from command import FlushCommand
from constants import BUFFER_FILE_PATH, MAX_CMD_BUFFER


class BufferManager:
    def __init__(self):
        pass

    def run_flush_command(self):
        FlushCommand("F").execute()

    def list_to_str(self, list_value):
        return ' '.join(map(str, list_value))

    def run(self, args):
        cmd_list = []
        is_flush = False
        if os.path.exists(BUFFER_FILE_PATH):
            with open(BUFFER_FILE_PATH, 'r') as f:
                args_list = f.readlines()
                for line in args_list:
                    cmd_list.append(line)

                if len(cmd_list) >= MAX_CMD_BUFFER:
                    self.run_flush_command()
                    is_flush = True

        with open(BUFFER_FILE_PATH, 'a') as f:
            if is_flush:
                f.truncate(0)
            f.write(self.list_to_str(args) + "\n")
