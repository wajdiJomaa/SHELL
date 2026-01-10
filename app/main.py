import sys

built_ins = {
    "echo",
    "exit",
    "type"
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
            sys.exit(0)
        elif scanned_command[0] == "echo":
            for i in range (1, len(scanned_command)):
                print(scanned_command[i], end=" ")
            
            print()
        elif scanned_command[0] == "type":
            if scanned_command[1] in built_ins:
                print(f"{scanned_command[1]} is a shell builtin")
            else:
                print(f"{scanned_command[1]}: not found")
        else:
            print(f"{command}: command not found")



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
