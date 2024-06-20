import os.path
from file_io import FileIO

from command import Command, FlushCommand, ReadCommand, WriteCommand, EraseCommand
from constants import BUFFER_FILE_PATH, MAX_CMD_BUFFER, INVALID_COMMAND, RESULT_FILE_PATH


class BufferManager:
    def __init__(self):
        pass

    def run_flush_command(self):
        FlushCommand(["F"]).execute()

    def run(self, cmd: Command):
        cmd_list = []
        if os.path.exists(BUFFER_FILE_PATH):
            with open(BUFFER_FILE_PATH, 'r') as f:
                cmd_list = [line.strip() for line in f.readlines()]

                if len(cmd_list) >= MAX_CMD_BUFFER:
                    self.run_flush_command()
                    cmd_list = []

        optimized_cmd_list = self.optimize_command_buffer(cmd_list, cmd)
        buffer_content = '\n'.join(optimized_cmd_list)

        with open(BUFFER_FILE_PATH, 'w') as f:
            f.truncate(0)
            f.write(buffer_content)

    def optimize_command_buffer(self, cmd_list, current_cmd: Command):
        if isinstance(current_cmd, ReadCommand):
            return self.optimize_command_buffer_for_read(cmd_list, current_cmd)
        elif isinstance(current_cmd, WriteCommand):
            return self.optimize_command_buffer_for_write(cmd_list, current_cmd)
        elif isinstance(current_cmd, EraseCommand):
            return self.optimize_command_buffer_for_erase(cmd_list, current_cmd)
        else:
            raise Exception(INVALID_COMMAND)

    def optimize_command_buffer_for_read(self, cmd_list, current_cmd: ReadCommand):
        if len(cmd_list) == 0:
            current_cmd.execute()
            return cmd_list

        for cmd in cmd_list:
            cmd_split = cmd.split()
            if cmd_split[0] == "W":
                if cmd_split[1] == current_cmd.lba:
                    FileIO(RESULT_FILE_PATH).save(cmd_split[2])
                    return cmd_list
            elif cmd_split[0] == "E":
                if self.is_read_lba_in_erase_lab_range(cmd_split.lba, current_cmd.lba):
                    FileIO(RESULT_FILE_PATH).save("0x00000000")
                    return cmd_list

        current_cmd.execute()
        return cmd_list

    def is_read_lba_in_erase_lab_range(self, cmd_split, lba):
        return int(lba) in range(int(cmd_split[1]), int(cmd_split[1]) + int(cmd_split[2]) + 1)

    def optimize_command_buffer_for_write(self, cmd_list, current_cmd: Command):
        # TODO
        return cmd_list + [current_cmd.serialize()]

    def optimize_command_buffer_for_erase(self, cmd_list, current_cmd: Command):
        # TODO
        return cmd_list + [current_cmd.serialize()]
