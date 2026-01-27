class Command:
    def __init__(self, command, stdin = None):
        self.command = command
        self.stdin = None

    def __repr__():
        return f"Command {self.command}"        

class Redirect:
    def __init__(self, command, redirect, type):
        self.command = command
        self.redirect = redirect
        self.type = type

    def __repr__():
        return f"Redirect {self.command} > {self.redirect}"
    
class Pipe:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__():
        return f"Pipe {self.left} | {self.right}"
    
