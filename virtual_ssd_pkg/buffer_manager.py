import os.path

from command import FlushCommand
from constants import BUFFER_FILE_PATH, MAX_CMD_BUFFER


class BufferManager:
    def __init__(self):
        pass

    def run_flush_command(self):
        FlushCommand(["F"]).execute()

    def list_to_str(self, list_value):
        return ' '.join(map(str, list_value))

    def run(self, args):
        cmd_list = []
        is_flush = False
        if os.path.exists(BUFFER_FILE_PATH):
            with open(BUFFER_FILE_PATH, 'r') as f:
                cmd_list = f.readlines()

                if len(cmd_list) >= MAX_CMD_BUFFER:
                    self.run_flush_command()
                    is_flush = True

        with open(BUFFER_FILE_PATH, 'a') as f:
            if is_flush:
                f.truncate(0)
            else:
                self.check_buffer_list(cmd_list, self.list_to_str(args))
            f.write(self.list_to_str(args) + "\n")

    def check_buffer_list(self, cmd_list, cur_cmd):
        # To-DO: Buffer 최적화 요소 추가
        pass
