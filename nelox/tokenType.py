from enum import Enum, auto


class TokenType(Enum):
    ATOM = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SLASH = auto()
    STAR = auto()

    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    SET = auto()
    AND = auto()
    FALSE = auto()
    FUNC = auto()
    FOR = auto()
    IF = auto()
    LIST = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    TRUE = auto()
    WHILE = auto()

    EOF = auto()
