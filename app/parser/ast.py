class Command:
    def __init__(self, command):
        self.command = command

    def __repr__():
        return f"Command {self.command}"        

class Redirect:
    def __init__(self, command, redirect):
        self.command = command
        self.redirect = redirect

    def __repr__():
        return f"Redirect {self.command} > {self.redirect}"
    
    
