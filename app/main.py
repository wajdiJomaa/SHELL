import sys
import os 
import subprocess
from app.scanner.scanner import Scanner
from app.parser.parser import Parser
from app.executor.executor import Executor
import readline
from app.completer.complete import complete
from app.history import History

class SHELL: 
    def run(self):
        readline.set_completer(complete)
        readline.parse_and_bind("tab: complete")
        hist = History()

        histfile = os.environ.get("HISTFILE", None)
        if histfile is not None:
            with open(histfile, "r") as f:
                for line in f:
                    if line.strip(" \n")!="":
                        hist.add(line.strip(" \n"))

        while True:
            try:
                command = input("$ ")
            except EOFError:
                sys.exit()
            
            hist.add(command)
            tokens = Scanner().scan(command)
            ast = Parser(tokens).parse()
            Executor(ast, hist).execute()

    
if __name__ == "__main__":
    SHELL().run()
