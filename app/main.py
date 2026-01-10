import sys


def main():
    while True:
        sys.stdout.write("$ ")
        try:
            command = input()
        except EOFError:
            break
        print(f"{command}: command not found")

if __name__ == "__main__":
    main()
