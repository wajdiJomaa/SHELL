import sys
from app.parser.ast import *
import os
import subprocess

class Executor:
    def __init__(self, ast):
        self.ast = ast
        self.built_ins = {
            "echo": self.execute__echo,
            "exit" : self.execute_exit,
            "type" : self.execute_type,
            "pwd" : self.execute_pwd,
            "cd": self.execute_cd
        }

    def execute(self):
        if isinstance(self.ast, Command):
            self.execute_command(self.ast)
        elif isinstance(self.ast, Redirect):
            self.execute_redirect(self.ast)

    def execute_command(self, command):
        if len(command.command) < 1:
            return

        if command.command[0].value in self.built_ins:
            self.built_ins[command.command[0].value](command.command)
        elif self.check_in_path(command.command[0].value) is not None:
            self.execute_from_path(list(map(lambda token: token.value, command.command)))
        else:
            print(f"{command.command[0].value}: command not found")


    def execute_from_path(self, scanned_command):
        result = subprocess.run(scanned_command)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

    def execute_type(self, scanned_command):
        if scanned_command[1].value in self.built_ins:
            print(f"{scanned_command[1].value} is a shell builtin")
        elif (p := self.check_in_path(scanned_command[1].value)) is not None:
            print(f"{scanned_command[1].value} is {p}")
        else:
            print(f"{scanned_command[1].value}: not found")


    def check_in_path(self,command):
        paths = os.environ.get("PATH", "").split(os.pathsep)
        for path in paths:
            if os.path.isdir(path) is False:
                continue

            full_path = os.path.join(path, command)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path
        
        return None

    def execute_exit(self, _):
        sys.exit(0)

    def execute__echo(self, scanned_command):
        for i in range (1, len(scanned_command)):
            print(scanned_command[i].value, end=" ")
        
        print()


    def execute_pwd(self, scanned_command):
        print(os.getcwd())
    
    def execute_cd(self, scanned_command, current_dir=None, index=0):
        if current_dir is None:
            current_dir = os.getcwd()
        
        if index == 0 and scanned_command[1].value.startswith("~") and scanned_command[1].is_quoted is False:
            index_slash = self.index_of_next_slash(scanned_command[1].value)
            if index_slash == -1 or index_slash >= len(scanned_command[1].value):
                os.chdir(os.getenv('HOME'))
                return
        
        scanned_command[1].value = scanned_command[1].value[index:]
        if len(scanned_command) < 2:
            os.chdir(os.getenv('HOME'))
            return

        if scanned_command[1].value.startswith("/"):
            if os.path.isdir(scanned_command[1].value):
                os.chdir(scanned_command[1].value)
            else:
                print(f"cd: {scanned_command[1].value}: No such file or directory") 
            return 
        
        index_slash = self.index_of_next_slash(scanned_command[1].value)
        if scanned_command[1].value.startswith(".."):
            if len(scanned_command[1].value) > 2 and scanned_command[1].value[2] != "/":
                new_path = os.path.join(current_dir, scanned_command[1].value[0:index_slash if index_slash != -1 else len(scanned_command[1].value)])
            else:
                new_path = os.path.dirname(current_dir)
        elif scanned_command[1].value.startswith("."):
            if len(scanned_command[1].value) > 1 and scanned_command[1].value[1] != "/":
                new_path = os.path.join(current_dir, scanned_command[1].value[0:index_slash if index_slash != -1 else len(scanned_command[1].value)])
            else:
                new_path = current_dir
        else:
            new_path = os.path.join(current_dir, scanned_command[1].value[0:index_slash if index_slash != -1 else len(scanned_command[1].value)])
        
        if os.path.isdir(new_path):
            if index_slash == -1 or index_slash >= len(scanned_command[1].value):
                os.chdir(new_path)
            else:
                self.execute_cd(scanned_command, new_path, index_slash + 1)
        else:
            print(f"cd: {scanned_command[1].value}: No such file or directory")

    def index_of_next_slash(self, path):
        is_slash = False
        index_slash = -1
        for i in range(len(path)):
            if path[i] == "/":
                is_slash = True
                index_slash = i
            elif is_slash is True:
                return index_slash
        return index_slash


    
    def execute_redirect(self, redirect):
        with open(redirect.redirect.value, "w") as f:
            old_stdout = sys.stdout
            sys.stdout = f
            try:
                self.execute_command(redirect.command)
            finally:
                sys.stdout = old_stdout