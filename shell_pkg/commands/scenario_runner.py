import os
import subprocess
from shell_pkg.commands.command import Command
from shell_pkg.constants import INVALID_COMMAND, SHELL_FILE_PATH


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
        process = subprocess.Popen(['python', self.__shell_file_path],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
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
