from virtual_ssd_pkg.constants import BUFFER_FILE_PATH


class BufferManager:
    def __init__(self):
        pass

    def insert_cmd_to_buffer(self, cmd):
        # TO-DO: when max buffer
        # cmd_list = []
        # with open(BUFFER_FILE_PATH, 'r') as file:
        #     for line in file:
        #         cmd_list.append(line)
        # if line >= MAX_CMD_BUFFER:
        #     return FlushCommand()

        with open(BUFFER_FILE_PATH, 'w') as file:
            file.write(cmd)
