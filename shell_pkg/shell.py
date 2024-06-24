import os
import sys
import importlib.util
from constants import COMMAND_DIR_PATH, ROOT_PATH, INVALID_COMMAND
sys.path.append(ROOT_PATH)
from logger_pkg.logger import Logger
from commands.invalid_command import InvalidCommand
from commands.scenario_runner import ScenarioRunner

class Shell(Logger):
    def run(self):
        if len(sys.argv) == 1:
            is_exit = 0
            while not is_exit:
                try:
                    print('> ', end='')
                    args = input().split()
                    cmd = self.determine_cmd(args)
                    is_exit = cmd.execute()
                except Exception as e:
                    self.print(e)
        elif len(sys.argv) == 2:
            cmd = ScenarioRunner([sys.argv[1]])
            cmd.execute()
        else:
            raise Exception(INVALID_COMMAND)

    def get_class_name(self, name: str):
        components = name.split('_')
        class_name = ''.join(x.title() for x in components)
        return class_name

    def get_command_module(self, args):
        for filename in os.listdir(COMMAND_DIR_PATH):
            if filename.endswith('.py'):
                module_name = filename[:-3].split('_command')[0]
                if module_name == args[0]:
                    module_path = os.path.join(COMMAND_DIR_PATH, filename)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, self.get_class_name(filename[:-3])):
                        return getattr(module, self.get_class_name(filename[:-3]))(args)

        return InvalidCommand()

    def determine_cmd(self, args):
        if len(args) == 0:
            return InvalidCommand()

        return self.get_command_module(args)


if __name__ == '__main__':
    shell = Shell()
    try:
        shell.run()
    except Exception as e:
        Logger().print(e)