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
        
        while self.current < len(self.tokens) and (self.tokens[self.current].t == TokenType.REDIRECT or self.tokens[self.current].t == TokenType.ERROR_REDIRECT 
                                    or self.tokens[self.current].t == TokenType.REDIRECT_APPEND or self.tokens[self.current].t == TokenType.REDIRECT_ERROR_APPEND):
            self.current += 1
            
            if self.current >= len(self.tokens):
                raise Exception("Expected a file name")

            redirect_target = self.tokens[self.current]
            command = Redirect(command, redirect_target, self.tokens[self.current - 1].t)
            self.current+=1

        return command
    
    def parse_command(self):
        res = []
        while self.current < len(self.tokens) and self.tokens[self.current].t == TokenType.NORMAL:
            res.append(self.tokens[self.current])
            self.current += 1
        return Command(res)