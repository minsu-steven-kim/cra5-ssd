class VirtualSSD:
    def __init__(self):
        pass

    def parsing_command(self, cmd):
        if type(cmd) == str:
            cmd_list = cmd.split(' ')
            if self.is_valid_read_command(cmd_list):
                return "READ"
            elif self.is_valid_write_command(cmd_list):
                return "WRITE"
            else:
                raise ValueError("INVALID COMMAND")
        else:
            raise ValueError("INVALID COMMAND")

    def is_valid_write_command(self, cmd_list):
        return len(cmd_list) == 4 and cmd_list[0:2] == ['ssd', 'W'] and\
            self.valid_LBA(cmd_list[2]) and self.valid_value(cmd_list[3])

    def is_valid_read_command(self, cmd_list):
        return len(cmd_list) == 3 and cmd_list[0:2] == ['ssd', 'R'] and \
            self.valid_LBA(cmd_list[2])

    def valid_LBA(self, LBA):
        if LBA.isdigit():
            if 0 <= int(LBA) and int(LBA) <= 99:
                return True
        return False

    def valid_value(self, value):
        if value.startswith('0x') and len(value) == 10:
            return True
        return False
