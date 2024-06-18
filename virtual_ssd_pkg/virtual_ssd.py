class VirtualSSD:
    def __init__(self):
        pass

    def parsing_command(self, cmd):
        if type(cmd) == str:
            cmd_list = cmd.split(' ')
            if len(cmd_list) == 3 and cmd_list[0:2] == ['ssd', 'R']:
                pass
            elif len(cmd_list) == 4 and cmd_list[0:2] == ['ssd', 'W']:
                pass
            else:
                raise ValueError("INVALID COMMAND")
        else:
            raise ValueError("INVALID COMMAND")


