from dataclasses import dataclass
from typing import Final
from enum import Enum,auto

# Token Types
class TokenType(Enum):
    # Single character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    COLON = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    POS_ARGS = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    FORM_STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    BOOLEN = auto()

    # Types
    TYPE_STRING = auto()
    TYPE_INTEGER = auto()
    TYPE_FLOAT = auto()
    TYPE_BOOLEN = auto()

    # Keywords
    AND = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NULL = auto()
    OR = auto()
    PRINT = auto()
    PRINTLN = auto()
    RETURN = auto()
    WHILE = auto()
    TRUE = auto()
    RAISE = auto()

    # Protocols
    HTTP = auto()
    FTP = auto()
    STMP = auto()
    TCP = auto()
    IP = auto()
    SSL = auto()

    # End of line obv LOL
    EOF = auto()

# Token Type Metaclass
@dataclass
class Token:
    type: Final[TokenType]
    lexeme: Final[str]
    literal: Final[object]
    line: Final[int]
    def __dbgrepr__(self) -> str:
        return f"<{self.type}:{self.lexeme} value=< {self.literal} >"
    def __repr__(self) -> str:
        return self.type.name