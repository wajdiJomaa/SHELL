import sys


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
