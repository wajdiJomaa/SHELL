from app.scanner.token import Token
from app.scanner.token_type import TokenType
from .ast import Command, Redirect

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.parse_redirect()
    
    def parse_redirect(self):
        command = self.parse_command()
        if self.current < len(self.tokens) and self.tokens[self.current].t == TokenType.REDIRECT:
            self.current += 1
            
            if self.current >= len(self.tokens):
                raise Exception("Expected a file name")

            redirect = self.tokens[self.current]
            return Redirect(command, redirect)
        return command
    
    def parse_command(self):
        res = []
        while self.current < len(self.tokens) and self.tokens[self.current].t == TokenType.NORMAL:
            res.append(self.tokens[self.current])
            self.current += 1
        return Command(res)