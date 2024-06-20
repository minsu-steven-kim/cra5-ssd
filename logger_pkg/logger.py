from datetime import datetime
import inspect
import os
class Logger:
    def print(self, log:str):
        now = datetime.now()
        dateFormat = now.strftime("%d.%m.%y %H:%M")
        method_name = inspect.currentframe().f_back.f_code.co_name
        formmatedMathod = f'{self.__class__.__name__}.{method_name}()'
        fomattedLog = f'[{dateFormat}] {formmatedMathod:<30} : {log}'
        self.displayLog(fomattedLog)

        filePath = './latest.log'
        newPath = f'until_{now.strftime("%y%m%d_%Hh_%Mm_%Ss")}.log'
        if os.path.exists(filePath):
            fileSize = os.path.getsize(filePath)
            if fileSize >= 10240:
                os.rename(filePath, newPath)
        self.saveLog(filePath, fomattedLog)
    def displayLog(self, fomattedLog:str):
        print(fomattedLog)
    def saveLog(self, filePath, log:str):
        with open(filePath, 'a') as f:
            f.write(log+'\n')