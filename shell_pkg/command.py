from abc import ABC, abstractmethod
import re
import os
import io
import sys
import subprocess

current_dir = os.path.dirname(__file__)
ROOT_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(ROOT_dir)


from logger_pkg.logger import Logger
from constants import SSD_FILE_PATH, RESULT_FILE_PATH, INVALID_COMMAND, HELP_MESSAGE, \
    MIN_LBA, MAX_LBA, MIN_ERASE_SIZE, MAX_ERASE_SIZE, MAX_SIZE_PER_COMMAND, , SHELL_FILE_PATH

class Command(ABC, Logger):
    @abstractmethod
    def execute(self):
        pass

    def is_invalid_lba(self, lba: str):
        if type(lba) != str:
            return True
        if not lba.isdigit():
            return True
        if MIN_LBA > int(lba) or int(lba) > MAX_LBA:
            return True
        return False

    def run_command(self, cmd):
        os.system(cmd)

    def is_invalid_value(self, value: str):
        if type(value) != str:
            return True
        return not bool(re.match(r'^0x[0-9A-F]{8}$', value))


class ExitCommand(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)

    def execute(self):
        return 1


class HelpCommand(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)

    def execute(self):
        self.print(HELP_MESSAGE)
        return 0


class InvalidCommand(Command):
    def execute(self):
        self.print(INVALID_COMMAND)
        return 0


class WriteCommand(Command):
    def __init__(self, args):
        if len(args) != 3:
            raise Exception(INVALID_COMMAND)
        self.__lba = args[1]
        self.__value = args[2]
        self.__file_path = SSD_FILE_PATH

    def get_lba(self):
        return self.__lba

    def set_lba(self, lba):
        self.__lba = lba

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def get_file_path(self):
        return self.__file_path

    def set_file_path(self, file_path):
        self.__file_path = file_path

    def execute(self):
        if self.is_invalid_parameter():
            raise Exception(INVALID_COMMAND)
        if not os.path.exists(self.__file_path):
            raise FileExistsError("VIRTUAL_SSD_PATH_ERROR")

        cmd = self.get_write_cmd_line()
        self.run_command(cmd)

    def is_invalid_parameter(self):
        if self.is_invalid_lba(self.__lba):
            return True
        if self.is_invalid_value(self.__value):
            return True
        return False

    def get_write_cmd_line(self):
        return f"python {self.__file_path} W {self.__lba} {self.__value}"


class EraseCommand(Command):
    def __init__(self, args):
        if len(args) != 3:
            raise Exception(INVALID_COMMAND)
        self.__lba = args[1]
        self.__size = args[2]
        self.__file_path = SSD_FILE_PATH

    def is_invalid_size(self, size: str):
        if type(size) != str:
            return True
        if not size.isdigit():
            return True
        if MIN_ERASE_SIZE > int(size) or MAX_ERASE_SIZE < int(size):
            return True
        return False

    def generate_commands(self):
        commands = []
        size = int(self.__size)
        lba = int(self.__lba)

        while size > 0:
            current_size = min(size, MAX_SIZE_PER_COMMAND)

            if lba > MAX_LBA:
                break
            if lba + current_size > 100:
                current_size = 100 - lba

            commands.append(self.get_write_cmd_line(str(lba), str(current_size)))
            lba += current_size
            size -= current_size

        return commands

    def execute(self):
        if self.is_invalid_parameter():
            raise Exception(INVALID_COMMAND)
        if not os.path.exists(self.__file_path):
            raise FileExistsError("VIRTUAL_SSD_PATH_ERROR")

        commands = self.generate_commands()

        for command in commands:
            self.run_command(command)

    def is_invalid_parameter(self):
        if self.is_invalid_lba(self.__lba):
            return True
        if self.is_invalid_size(self.__size):
            return True
        return False

    def get_write_cmd_line(self, lba, size):
        return f"python {self.__file_path} E {lba} {size}"


class EraseRangeCommand(Command):
    def __init__(self, args):
        if len(args) != 3:
            raise Exception(INVALID_COMMAND)
        self.__start_lba = args[1]
        self.__end_lba = args[2]
        self.__file_path = SSD_FILE_PATH

    def is_invalid_end_lba(self, start_lba: str, end_lba: str):
        if int(start_lba) > int(end_lba):
            return True
        return False

    def generate_commands(self):
        commands = []
        size = int(self.__end_lba) - int(self.__start_lba)
        lba = int(self.__start_lba)

        while size > 0:
            current_size = min(size, MAX_SIZE_PER_COMMAND)

            if lba > MAX_LBA:
                break

            if lba + current_size > 100:
                current_size = 100 - lba

            commands.append([str(lba), str(current_size)])
            lba += current_size
            size -= current_size

        return commands

    def execute(self):
        if self.is_invalid_parameter():
            raise Exception(INVALID_COMMAND)
        if not os.path.exists(self.__file_path):
            raise FileExistsError("VIRTUAL_SSD_PATH_ERROR")

        commands = self.generate_commands()

        for command in commands:
            EraseCommand(['erase', command[0], command[1]]).execute()

    def is_invalid_parameter(self):
        if self.is_invalid_lba(self.__start_lba):
            return True
        if self.is_invalid_lba(self.__end_lba):
            return True
        if self.is_invalid_end_lba(self.__start_lba, self.__end_lba):
            return True
        return False


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


class FullwriteCommand(Command):
    def __init__(self, args):
        if len(args) != 2:
            raise Exception(INVALID_COMMAND)
        self.__value = args[1]
        self.__filepath = SSD_FILE_PATH

    def execute(self):
        if self.is_invalid_value(self.__value):
            raise Exception(INVALID_COMMAND)

        for lba in range(MAX_LBA + 1):
            WriteCommand(['write', str(lba), self.__value]).execute()


class FullreadCommand(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)

    def execute(self):
        for lba in range(MAX_LBA + 1):
            read_cmd = ReadCommand(['read', str(lba)])
            read_cmd.execute()


class TestApp1Command(Command):
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


class TestApp2Command(Command):
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

class ScenarioRunner(Command):
    def __init__(self, args):
        if len(args) != 1:
            raise Exception(INVALID_COMMAND)
        self.__file_path = args[0]
        self.__shell_file_path = SHELL_FILE_PATH

    def execute(self):
        if not os.path.exists(self.__file_path):
            raise FileExistsError("SCENARIO_FILE_PATH_ERROR")
        if not os.path.exists(self.__shell_file_path):
            raise FileExistsError("SCENARIO_FILE_PATH_ERROR")

        scenario = self.get_scenario()
        self.execute_script_in_scenario(scenario)

    def execute_script_in_scenario(self, scenario):
        for script in scenario:
            script = script.strip()
            stdout = self.call_shell_subprocess(script)
            if self.executed_successfully(script, stdout):
                self.print_success_log(script)
            else:
                self.print_fail_log(script)
                break

    def get_scenario(self):
        with open(self.__file_path, 'r') as f:
            scenario = f.readlines()
        return scenario

    def call_shell_subprocess(self, script):
        process = subprocess.Popen(['python', self.__shell_file_path], \
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
                                   text=True)
        subprocess_cmd = script + '\nexit\n'
        self.print_execute_script_log(script)
        stdout, stderr = process.communicate(input=subprocess_cmd)
        return stdout

    def print_execute_script_log(self, script):
        print(f'{script} --- Run...', end='')

    def executed_successfully(self, script, output):
        if f'{script} : Success' in output:
            return True
        else:
            return False

    def print_success_log(self, script):
        print('Pass')

    def print_fail_log(self, script):
        print('FAIL!')