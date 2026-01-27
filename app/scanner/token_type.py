from enum import Enum, auto

class TokenType(Enum):
    NORMAL = auto()
    REDIRECT = auto()
    ERROR_REDIRECT = auto()
    REDIRECT_APPEND = auto()
    REDIRECT_ERROR_APPEND = auto()
    PIPE = auto()