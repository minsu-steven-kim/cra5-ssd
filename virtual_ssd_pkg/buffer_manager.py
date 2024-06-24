import os.path
from file_io import FileIO

from command import Command, FlushCommand, ReadCommand, WriteCommand, EraseCommand, CommandFactory
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
            if self.is_read_lba_in_write_lba(cmd_split, current_cmd.lba):
                FileIO(RESULT_FILE_PATH).save(cmd_split[2])
                return cmd_list
            if self.is_read_lba_in_erase_lab_range(cmd_split, current_cmd.lba):
                FileIO(RESULT_FILE_PATH).save("0x00000000")
                return cmd_list

        current_cmd.execute()
        return cmd_list

    def is_read_lba_in_write_lba(self, cmd_split, cur_lba):
        if cmd_split[0] != "W":
            return False
        return cmd_split[1] == cur_lba

    def is_read_lba_in_erase_lab_range(self, cmd_split, cur_lba):
        if cmd_split[0] != "E":
            return False
        return int(cur_lba) in range(int(cmd_split[1]), int(cmd_split[1]) + int(cmd_split[2]) + 1)

    def optimize_command_buffer_for_write(self, cmd_list, curr: WriteCommand):
        cmd_list = [CommandFactory().create_command(args.split()) for args in cmd_list]
        optimized = []

        def process_prev_write(before: WriteCommand):
            if int(before.lba) == int(curr.lba):
                return []
            return [before]

        def create_erase_command(start: int, end: int):
            if start < end:
                return EraseCommand(['E', str(start), str(end - start)])
            else:
                return None

        def process_prev_erase(before: EraseCommand):
            before_lba = int(before.lba)
            before_size = int(before.size)
            curr_lba = int(curr.lba)

            if not before_lba <= curr_lba < (before_lba + before_size):
                return [before]

            left_erase = create_erase_command(before_lba, curr_lba)
            right_erase = create_erase_command(curr_lba + 1, before_lba + before_size)

            ret = []
            if left_erase is not None:
                ret.append(left_erase)
            if right_erase is not None:
                ret.append(right_erase)
            return ret

        for prev in cmd_list:
            if isinstance(prev, WriteCommand):
                optimized += process_prev_write(prev)
            elif isinstance(prev, EraseCommand):
                optimized += process_prev_erase(prev)
            else:
                optimized += [prev]

        return [cmd.serialize() for cmd in optimized] + [curr.serialize()]

    def optimize_command_buffer_for_erase(self, cmd_list, current_cmd: Command):
        # TODO
        return cmd_list + [current_cmd.serialize()]
