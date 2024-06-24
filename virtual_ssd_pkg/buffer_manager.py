import os.path

from command import Command, FlushCommand, ReadCommand, WriteCommand, EraseCommand, CommandFactory
from constants import BUFFER_FILE_PATH, MAX_CMD_BUFFER, INVALID_COMMAND


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

    def optimize_command_buffer_for_read(self, cmd_list, current_cmd: Command):
        # TODO
        return cmd_list + [current_cmd.serialize()]

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

    def optimize_command_buffer_for_erase(self, cmd_list, current_cmd: EraseCommand):
        def make_one_erase_list(erase_bit, loc):
            len = 0
            for i in range(loc, 100):
                if len == 10:
                    break
                if erase_bit[i] == 1:
                    erase_bit[i] = 0
                    len += 1
                    continue
                break
            return erase_bit, f"E {loc} {len}"

        def make_erase_list(erase_bit):
            ret_list = []
            for loc in range(0, 100):
                if erase_bit[loc] == 1:
                    erase_bit, tmp = make_one_erase_list(erase_bit, loc)
                    ret_list.append(tmp)
            return ret_list

        cur_lba = int(current_cmd.lba)
        cur_size = int(current_cmd.size)

        original_cur_lba = cur_lba
        original_cur_end = cur_lba + cur_size

        ret_list = []
        erase_bit = [0] * 100

        for i in range(len(cmd_list)):
            past_cmd = cmd_list[i]
            if past_cmd == '':
                continue
            past_cmd_args = past_cmd.split()  # ['E',str(lba),str(size)] or ['W',str(lba),str(0x12341234)]

            if past_cmd_args[0] == 'W':
                past_lba = int(past_cmd_args[1])
                if original_cur_lba <= past_lba < original_cur_end:  # refactoring 필요
                    pass
                else:
                    ret_list.append(cmd_list[i])

            if past_cmd_args[0] == 'E':
                past_lba = int(past_cmd_args[1])
                past_size = int(past_cmd_args[2])
                for i in range(past_lba, past_lba + past_size):
                    erase_bit[i] = 1

        for i in range(cur_lba, cur_lba + cur_size):
            erase_bit[i] = 1

        ret_list += make_erase_list(erase_bit)

        return ret_list
