import sys
import io
from shell_pkg.commands.command import Command
from shell_pkg.commands.fullread_command import FullreadCommand
from shell_pkg.commands.fullwrite_command import FullwriteCommand
from shell_pkg.constants import INVALID_COMMAND, MAX_LBA



class Testapp1Command(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)
        self.testValue = '0xABCDFFFF'
        self.validationValue = '0xABCDFFFF\n' * (MAX_LBA + 1)

    def execute(self):
        self.fullwrite()
        result = self.fullread()
        self.evaluate_result(result)

    def fullread(self):
        buffer = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = buffer

        fullRead = FullreadCommand(['fullread'])
        fullRead.execute()

        sys.stdout = original_stdout
        result = buffer.getvalue()

        print(result)
        buffer.close()
        return result

    def fullwrite(self):
        fullWrite = FullwriteCommand(['fullwrite', self.testValue])
        fullWrite.execute()

    def evaluate_result(self, result):
        if self.validationValue == result:
            print("testapp1 : Success")
        else:
            print("testapp1 : Fail")