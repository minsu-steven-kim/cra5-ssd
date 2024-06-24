from datetime import datetime
import inspect
import os

MAX_FILE_SIZE = 10240


class Logger:
    def print(self, log: str):
        self.logPath = './latest.log'
        self.displayLog(log)
        self.saveLog(self.make_log(log))

    def get_logDate(self):
        return datetime.now().strftime("%y.%m.%d %H:%M")
    def get_fileDate(self):
        return datetime.now().strftime("%y%m%d_%Hh_%Mm_%Ss")

    def get_methodFormat(self):
        method_name = inspect.currentframe().f_back.f_back.f_back.f_code.co_name
        if method_name == '<module>':
            method_name = 'main'
            class_name = os.path.basename(inspect.currentframe().f_back.f_back.f_back.f_globals["__file__"]).split('.')[0]
        else:
            class_name = self.__class__.__name__
        return f'{class_name}.{method_name}()'

    def displayLog(self, log: str):
        print(log)

    def make_log(self, log):
        return f'[{self.get_logDate()}] {self.get_methodFormat():<30} : {log}'

    def saveLog(self, fomattedLog):
        if os.path.exists(self.logPath):
            if os.path.getsize(self.logPath) >= MAX_FILE_SIZE:
                self.backup_logs()
        self.fileWrite(fomattedLog)

    def backup_logs(self):
        newPath = f'until_{self.get_fileDate()}.zip'
        os.rename(self.logPath, newPath)

    def fileWrite(self, log: str):
        with open(self.logPath, 'a') as f:
            f.write(log + '\n')