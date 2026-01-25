import sys
import os 
import subprocess
from app.scanner.scanner import Scanner
from app.parser.parser import Parser
from app.executor.executor import Executor
import readline
from app.completer.complete import complete
class SHELL: 
    def run(self):
        readline.set_completer(complete)
        readline.parse_and_bind("tab: complete")
        while True:
            try:
                command = input("$ ")
            except EOFError:
                sys.exit()
            
            tokens = Scanner().scan(command)
            ast = Parser(tokens).parse()
            Executor(ast).execute()

    
if __name__ == "__main__":
    SHELL().run()
