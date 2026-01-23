from .token import Token
from .token_type import TokenType

class Scanner:    
    def scan(self, command):
            current = 0
            result = []
            is_quoted = False
            is_double_quote = False
            while current < len(command):
                match command[current]:
                    case " ":
                        current += 1
                    case ">":
                        result.append(Token(">", t=TokenType.REDIRECT))
                        current += 1
                    case "1":
                        if len(command) > current + 1 and command[current + 1] == ">":
                            result.append(Token(">", t=TokenType.REDIRECT))
                            current += 2
                        else:
                            token, current = self.scan_token(command, current)
                            result.append(token)
                    case "2":
                        if len(command) > current + 1 and command[current + 1] == ">":
                            result.append(Token(">", t=TokenType.ERROR_REDIRECT))
                            current += 2
                        else:
                            token, current = self.scan_token(command, current)
                            result.append(token)
                    case _:
                        token, current = self.scan_token(command, current)
                        result.append(token)
            return result


    def scan_token(self, command, current):
        s = ""
        is_quoted = False
        is_double_quote = False
        while(current < len(command) and command[current] != " "):
            if command[current] == "\\":
                if current + 1 < len(command):
                    s += command[current + 1]
                    current += 2
                else:
                    current += 1
                continue
            if command[current] == "'":
                current += 1
                while(current < len(command) and command[current] != "'"):
                    s += command[current]
                    current += 1
                current += 1
                is_quoted = True
                continue
            if command[current] == '"':
                current += 1
                while(current < len(command) and command[current] != '"'):
                    if command[current] == "\\":
                        if current + 1 < len(command):
                            if command[current +1] == '"' or command[current + 1] == "\\":
                                current += 1
                    s += command[current]
                    current += 1
                current += 1
                is_quoted = True
                is_double_quote = True
                continue
            s += command[current]
            current += 1
        return Token(s, TokenType.NORMAL ,is_quoted, is_double_quote), current
