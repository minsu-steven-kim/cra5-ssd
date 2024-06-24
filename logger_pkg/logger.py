from datetime import datetime
import inspect
import os


class Logger:
    def print(self, log: str):
        now = datetime.now()
        dateFormat = now.strftime("%y.%m.%d %H:%M")
        method_name = inspect.currentframe().f_back.f_code.co_name
        import os
        from shell_pkg.commands.command import Command
        from shell_pkg.constants import INVALID_COMMAND, SSD_FILE_PATH, RESULT_FILE_PATH

        class ReadCommand(Command):
            def __init__(self, args):
                if not self.check_command_length(args):
                    raise Exception(INVALID_COMMAND)
                self.lba = args[1]
                self.ssd_filepath = SSD_FILE_PATH
                self.result_filepath = RESULT_FILE_PATH

            def check_command_length(self, args):
                if len(args) == 2:
                    return True
                return False

            def execute(self):
                if self.is_invalid_lba(self.lba):
                    raise Exception(INVALID_COMMAND)
                if not os.path.exists(self.ssd_filepath):
                    raise FileExistsError("VIRTUAL_SSD_PATH_ERROR")
                self.send_cmd_to_ssd()
                self.print(self.get_result_with_ssd())

            def get_result_with_ssd(self):
                with open(self.result_filepath, 'r') as f:
                    return f.read()

            def create_command(self):
                return f"python {self.ssd_filepath} R {self.lba}"

            def send_cmd_to_ssd(self):
                cmd = self.create_command()
                self.run_command(cmd)

        if method_name == '<module>':
            method_name = 'main'
            class_name = os.path.basename(inspect.currentframe().f_back.f_globals["__file__"]).split('.')[0]
        else:
            class_name = self.__class__.__name__
        formmatedMathod = f'{class_name}.{method_name}()'
        fomattedLog = f'[{dateFormat}] {formmatedMathod:<30} : {log}'
        self.displayLog(log)

        filePath = './latest.log'
        newPath = f'until_{now.strftime("%y%m%d_%Hh_%Mm_%Ss")}.zip'
        if os.path.exists(filePath):
            fileSize = os.path.getsize(filePath)
            if fileSize >= 10240:
                os.rename(filePath, newPath)
        self.saveLog(filePath, fomattedLog)

    def displayLog(self, fomattedLog: str):
        print(fomattedLog)

    def saveLog(self, filePath, log: str):
        with open(filePath, 'a') as f:
            f.write(log + '\n')