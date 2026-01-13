import sys
import os 
import subprocess
from token import Token

class SHELL:

    def __init__(self):
        
        self.built_ins = {
        "echo": self.execute__echo,
        "exit" : self.execute_exit,
        "type" : self.execute_type,
        "pwd" : self.execute_pwd,
        "cd": self.execute_cd
    }

    def run(self):
        while True:
            sys.stdout.write("$ ")
            try:
                command = input()
            except EOFError:
                sys.exit()
            
            scanned_command = self.scan(command.strip())

            if scanned_command[0].value in self.built_ins:
                self.built_ins[scanned_command[0].value](scanned_command)
            elif self.check_in_path(scanned_command[0].value) is not None:
                self.execute_from_path(list(map(lambda token: token.value, scanned_command)))
            else:
                print(f"{command}: command not found")


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



    def scan(self,command):
        current = 0
        result = []
        
        while current < len(command):
            match command[current]:
                case " ":
                    current += 1
                case "'":
                    current += 1
                    s = ""
                    while(current < len(command) and command[current] != "'"):
                        s += command[current]
                        current += 1

                    if current == len(command):
                        print("Unclosed quotation mark")
                    
                    current += 1
                    result.append(Token(s, is_quoted=True))
                case _:
                    s = ""
                    while(current < len(command) and command[current] != " "):
                        if command[current] == "'":
                            current += 1
                            while(current < len(command) and command[current] != "'"):
                                s += command[current]
                                current += 1
                            current += 1
                            continue
                        s += command[current]
                        current += 1
                    result.append(Token(s))

        return result

    def execute_pwd(self, scanned_command):
        print(os.getcwd())
    
    def execute_cd(self, scanned_command, current_dir=None, index=0):
        if current_dir is None:
            current_dir = os.getcwd()
        
        if index == 0 and scanned_command[1].value.startswith("~"):
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
                new_path = os.path.join(current_dir, scanned_command[1].value[0:index_slash if index_slash != -1 else len(scanned_command[1])])
            else:
                new_path = os.path.dirname(current_dir)
        elif scanned_command[1].value.startswith("."):
            if len(scanned_command[1].value) > 1 and scanned_command[1].value[1] != "/":
                new_path = os.path.join(current_dir, scanned_command[1].value[0:index_slash if index_slash != -1 else len(scanned_command[1])])
            else:
                new_path = current_dir
        else:
            new_path = os.path.join(current_dir, scanned_command[1].value[0:index_slash if index_slash != -1 else len(scanned_command[1])])
        
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
    
if __name__ == "__main__":
    def main():
        shell = SHELL()
        shell.run()
    main()
