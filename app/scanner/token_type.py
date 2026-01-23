from enum import Enum, auto

class TokenType(Enum):
    NORMAL = auto()
    REDIRECT = auto()
    ERROR_REDIRECT = auto()