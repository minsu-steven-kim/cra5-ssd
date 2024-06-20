from datetime import datetime
import inspect
import os


class Logger:
    def print(self, log: str):
        now = datetime.now()
        dateFormat = now.strftime("%y.%m.%d %H:%M")
        method_name = inspect.currentframe().f_back.f_code.co_name
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