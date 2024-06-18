class VirtualSSD:
    def __init__(self):
        pass

    def parsing_command(self, cmd):
        if type(cmd) == str:
            cmd_list = cmd.split(' ')
            if len(cmd_list) == 3 and cmd_list[0:2] == ['ssd', 'R']:
                if self.valid_LBA(cmd_list[2]):
                    return "READ"
                else:
                    raise ValueError("INVALID COMMAND")
            elif len(cmd_list) == 4 and cmd_list[0:2] == ['ssd', 'W']:
                if self.valid_LBA(cmd_list[2]) and self.valid_value(cmd_list[3]):
                    return "WRITE"
                else:
                    raise ValueError("INVALID COMMAND")
            else:
                raise ValueError("INVALID COMMAND")
        else:
            raise ValueError("INVALID COMMAND")

    def valid_LBA(self, LBA):
        if LBA.isdigit():
            if 0 <= int(LBA) and int(LBA) <= 99:
                return True
        return False

    def valid_value(self, value):
        if value.startswith('0x') and len(value) == 10:
            return True
        return False
