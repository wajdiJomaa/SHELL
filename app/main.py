import sys
import os 
import subprocess

built_ins = {
    "echo",
    "exit",
    "type",
    "pwd"
}

def main():
    while True:
        sys.stdout.write("$ ")
        try:
            command = input()
        except EOFError:
            sys.exit()
        
        scanned_command = scan(command.strip())

        if scanned_command[0] == "exit":
            execute_exit()
        elif scanned_command[0] == "echo":
            execute__echo(scanned_command)
        elif scanned_command[0] == "type":
            execute_type(scanned_command)
        elif scanned_command[0] == "pwd":
            print(os.getcwd())
        elif check_in_path(scanned_command[0]) is not None:
            execute_from_path(scanned_command)
        else:
            print(f"{command}: command not found")


def execute_from_path(scanned_command):
    result = subprocess.run(scanned_command)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

def execute_type(scanned_command):
    if scanned_command[1] in built_ins:
        print(f"{scanned_command[1]} is a shell builtin")
    elif (p := check_in_path(scanned_command[1])) is not None:
        print(f"{scanned_command[1]} is {p}")
    else:
        print(f"{scanned_command[1]}: not found")


def check_in_path(command):
    paths = os.environ.get("PATH", "").split(os.pathsep)
    for path in paths:
        if os.path.isdir(path) is False:
            continue

        full_path = os.path.join(path, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    
    return None

def execute_exit():
    sys.exit(0)

def execute__echo(scanned_command):
    for i in range (1, len(scanned_command)):
        print(scanned_command[i], end=" ")
    
    print()



def scan(command):
    current = 0
    result = []
    
    while current < len(command):
        match command[current]:
            case " ":
                current += 1
            case _:
                s = ""
                while(current < len(command) and command[current] != " "):
                    s += command[current]
                    current += 1
                result.append(s)

    return result



if __name__ == "__main__":
    main()
