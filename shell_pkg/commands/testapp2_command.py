import sys
import io
from shell_pkg.commands.command import Command
from shell_pkg.commands.write_command import WriteCommand
from shell_pkg.commands.read_command import ReadCommand
from shell_pkg.constants import INVALID_COMMAND


class Testapp2Command(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)
        self.testValue1 = '0xAAAABBBB'
        self.testValue2 = '0x12345678'
        self.testLBAmax = 5
        self.test2Count = 30
        self.validationValue = '0x12345678\n' * (self.testLBAmax + 1)

    def execute(self):
        self.write_test1()
        self.write_test2()
        result = self.read_test()
        self.evaluate_result(result)

    def write_test1(self):
        args_list = [['write', str(i), self.testValue1] for i in range(self.testLBAmax + 1)]
        for args in args_list:
            write_command = WriteCommand(args)
            for i in range(self.test2Count):
                write_command.execute()

    def write_test2(self):
        args_list = [['write', str(i), self.testValue2] for i in range(self.testLBAmax + 1)]
        for args in args_list:
            write_command = WriteCommand(args)
            write_command.execute()

    def read_test(self):
        buffer = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = buffer

        args_list = [['read', str(i)] for i in range(self.testLBAmax + 1)]
        for args in args_list:
            read_command = ReadCommand(args)
            read_command.execute()

        sys.stdout = original_stdout
        result = buffer.getvalue()

        print(result)
        buffer.close()
        return result

    def evaluate_result(self, result):
        if self.validationValue == result:
            print("testapp2 : Success")
        else:
            print("testapp2 : Fail")
