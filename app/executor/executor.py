import sys
from app.parser.ast import *
import os
import subprocess
from ..scanner.token_type import TokenType
from ..scanner.token import Token
class Executor:
    def __init__(self, ast):
        self.ast = ast
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.stdin = sys.stdin
        self.built_ins = {
            "echo": self.execute__echo,
            "exit" : self.execute_exit,
            "type" : self.execute_type,
            "pwd" : self.execute_pwd,
            "cd": self.execute_cd
        }

    def execute(self):
        self._execute(self.ast)

    def _execute(self, ast):
        if isinstance(ast, Command):
            self.execute_command(ast)
        elif isinstance(ast, Redirect):
            self.execute_redirect(ast)
        elif isinstance(ast, Pipe):
            self.execute_pipe(ast)

    def execute_command(self, command):
        if len(command.command) < 1:
            return

        if command.command[0].value in self.built_ins:
            self.built_ins[command.command[0].value](command.command)
        elif self.check_in_path(command.command[0].value) is not None:
            self.execute_from_path(list(map(lambda token: token.value, command.command)))
        else:
            print(f"{command.command[0].value}: command not found", file=self.stderr)


    def execute_from_path(self, scanned_command):
        result = subprocess.run(scanned_command, stdin=self.stdin, stdout=self.stdout, stderr=self.stderr)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

    def execute_type(self, scanned_command):
        if scanned_command[1].value in self.built_ins:
            print(f"{scanned_command[1].value} is a shell builtin", file=self.stdout)
        elif (p := self.check_in_path(scanned_command[1].value)) is not None:
            print(f"{scanned_command[1].value} is {p}", file=self.stdout)
        else:
            print(f"{scanned_command[1].value}: not found", file=self.stderr)


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
            print(scanned_command[i].value, end=" " if i < len(scanned_command) - 1 else "", file=self.stdout)
        
        print(file=self.stdout)


    def execute_pwd(self, scanned_command):
        print(os.getcwd(), file=self.stdout)
    
    def execute_cd(self, scanned_command, current_dir=None, index=0):
        if len(scanned_command) < 2:
            os.chdir(os.getenv('HOME'))
            return
        
        if scanned_command[1].value.strip() == "":
            os.chdir(os.getcwd())
            return

        resolved_path = self.resolve_path(scanned_command[1].value)
        if os.path.isdir(resolved_path):
            os.chdir(resolved_path)
        else:
            print(f"cd: {scanned_command[1].value}: No such file or directory", file=self.stderr)

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
        resolved_path = self.resolve_path(redirect.redirect.value)
        if os.path.isdir(resolved_path):
            print(f"{redirect.redirect.value}: Is a directory", file=self.stderr)
            return
        
        if os.path.exists(os.path.dirname(resolved_path)) is False:
            print(f"{redirect.redirect.value} No such file or directory", file=self.stderr)
            return

        if redirect.type == TokenType.REDIRECT or redirect.type == TokenType.REDIRECT_APPEND:    
            old_stdout = self.stdout
            mode = "w" if redirect.type == TokenType.REDIRECT else "a"
            with open(resolved_path, mode) as f:
                try:
                    self.stdout = f
                    self._execute(redirect.command)
                finally:
                    self.stdout = old_stdout
        
        elif redirect.type == TokenType.ERROR_REDIRECT or redirect.type == TokenType.REDIRECT_ERROR_APPEND:
            old_stderr = self.stderr
            mode = "w" if redirect.type == TokenType.ERROR_REDIRECT else "a"
            with open(resolved_path, mode) as f:
                try:
                    self.stderr = f
                    self._execute(redirect.command)
                finally:
                    self.stderr = old_stderr
    def resolve_path(self, path, current_dir=None, index=0):
        if current_dir is None:
            current_dir = os.getcwd()

        if index >= len(path):
            return current_dir

        if path.startswith("/"):
            return path

        path = path[index:]
        
        index_slash = self.index_of_next_slash(path)
        if path.startswith(".."):
            if len(path) > 2 and path[2] != "/":
                new_path = os.path.join(current_dir, path[0:index_slash if index_slash != -1 else len(path)])
            else:
                new_path = os.path.dirname(current_dir)
        elif path.startswith("."):
            if len(path) > 1 and path[1] != "/":
                new_path = os.path.join(current_dir, path[0:index_slash if index_slash != -1 else len(path)])
            else:
                new_path = current_dir

        elif index == 0 and path.startswith("~"):
            if len(path) > 1 and path[1] != "/":
                new_path = os.path.join(current_dir, path[0:index_slash if index_slash != -1 else len(path)])
            else:
                new_path = os.getenv('HOME')
        else:
            new_path = os.path.join(current_dir, path[0:index_slash if index_slash != -1 else len(path)])
        
        return self.resolve_path(path, new_path, index_slash + 1 if index_slash != -1 else len(path))


    def execute_pipe(self, pipe):
        r,w = os.pipe()

        pid = os.fork()
        if pid == 0:
            os.close(r)
            with os.fdopen(w, "w") as f:
                self.stdout = f
                self._execute(pipe.left)
            exit(0)
        else:            
            os.close(w)
            old_stdin = self.stdin
            with os.fdopen(r, "r") as f:
                self.stdin = f
                self._execute(pipe.right)