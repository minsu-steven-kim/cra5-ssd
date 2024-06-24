import os.path

from command import Command, FlushCommand, ReadCommand, WriteCommand, EraseCommand
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

    def optimize_command_buffer_for_write(self, cmd_list, current_cmd: Command):
        # TODO
        return cmd_list + [current_cmd.serialize()]

    def optimize_command_buffer_for_erase(self, cmd_list, current_cmd: EraseCommand):
        cur_lba = current_cmd.lba
        cur_size = current_cmd.size

        original_cur_lba = cur_lba
        original_cur_end = cur_lba + cur_size

        ret_list = []
        finish_flag = False
        for i in range(len(cmd_list)):
            cur_end = cur_lba + cur_size
            past_cmd = cmd_list[i]
            if past_cmd == '':
                continue
            past_cmd_args = past_cmd.split()  # ['E',str(lba),str(size)] or ['W',str(lba),str(0x12341234)]

            if past_cmd_args[0] == 'W':
                past_lba = int(past_cmd_args[1])
                if original_cur_lba <= past_lba < original_cur_end:
                    pass
                else:
                    ret_list.append(cmd_list[i])
                continue

            if finish_flag:
                ret_list.append(cmd_list[i])
                continue

            elif past_cmd_args[0] == 'E':
                past_lba = int(past_cmd_args[1])
                past_size = int(past_cmd_args[2])
                past_end = past_lba + past_size

                # 서로 관계 없을 때
                if past_end < cur_lba or cur_end < past_lba:
                    ret_list.append(cmd_list[i])
                    continue

                # 한 쪽이 포함될 때
                # 현재가 과거에 완전 포함일 경우
                if past_lba <= cur_lba and cur_end <= past_lba:
                    ret_list.append(cmd_list[i])
                    finish_flag = True
                    continue

                    # 과거가 현재에 완전 포함일 경우
                if cur_lba <= past_lba and past_end <= cur_lba:
                    continue

                # 완벽히 붙을 때
                # 과거 - 현재 순일 때
                if past_end == cur_lba:
                    if past_size + cur_size == 10:
                        past_size = 10
                        finish_flag = True
                    elif past_size + cur_size > 10:
                        val = 10 - past_size
                        past_size = 10  ## update 되게 만들어야함
                        cur_size = cur_size - val
                        cur_lba = cur_lba + val
                    else:
                        past_size += cur_size
                        finish_flag = True
                    ret_list.append(f"E {past_lba} {past_size}")
                    continue

                    # 현재 - 과거 순일 때
                if cur_end == past_lba:
                    if past_size + cur_size == 10:
                        past_size = 10
                        past_lba -= cur_size
                        finish_flag = True
                    elif past_size + cur_size > 10:
                        val = 10 - past_size
                        past_size = 10
                        past_lba -= val
                        cur_size = cur_size - val
                    else:
                        past_lba -= cur_size
                        finish_flag = True
                    ret_list.append(f"E {past_lba} {past_size}")
                    continue

                # 그 외 그냥 겹치는 곳 있을 떼
                # 과거-(포함)-현재
                if past_lba < cur_lba:
                    total_size = cur_lba + cur_size - past_lba
                    if total_size > 10:
                        past_size = 10
                        cur_size = (cur_lba + cur_size) - (past_lba + past_size)
                        cur_lba = past_lba + past_size
                    elif total_size == 10:
                        past_size = 10
                        finish_flag = True
                    else:
                        past_size = total_size
                        finish_flag = True
                    ret_list.append(f"E {past_lba} {past_size}")
                    continue

                    # 현재 - (포함) - 과거
                if cur_lba < past_lba:
                    total_size = past_lba + past_size - cur_lba
                    if total_size > 10:
                        val = 10 - past_size
                        past_lba = past_lba - val
                        past_size = 10
                        cur_size -= val
                    elif total_size == 10:
                        past_size = 10
                        past_lba = cur_lba
                        finish_flag = True
                    else:
                        past_size = total_size
                        past_lba = cur_lba
                        finish_flag = True
                    ret_list.append(f"E {past_lba} {past_size}")
                    continue

            else:
                raise Exception(INVALID_COMMAND)
        if finish_flag == False:
            ret_list.append(f"E {cur_lba} {cur_size}")

        return ret_list
