import sys


def main():
    while True:
        sys.stdout.write("$ ")
        try:
            command = input()

            if command.strip() == "exit":
                sys.exit(0)


        except EOFError:
            sys.exit()
        
        print(f"{command}: command not found")

if __name__ == "__main__":
    main()
