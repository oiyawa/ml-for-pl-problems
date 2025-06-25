from typing import List

from nelox import Nelox
from token import Token
from tokenType import TokenType


def is_alpha_numeric(c):
    return c.is_alpha or c.is_digit


def is_alpha(c):
    return c.isalpha() or c == '_'


def is_digit(c):
    return '0' <= c <= '9'


class Scanner:
    keywords: dict[str, TokenType] = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "false": TokenType.FALSE,
        "func": TokenType.FUNC,
        "for": TokenType.FOR,
        "if": TokenType.IF,
        "list": TokenType.LIST,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "set": TokenType.SET,
        "true": TokenType.TRUE,
        "while": TokenType.WHILE
    }

    def __init__(self, source: str):
        self.source = None
        self.token = None
        self.source: str = source
        self.tokens: List[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.token

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def add_token(self, type: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def scan_token(self):
        c = self.advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == ',)':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            if self.match('='):
                self.add_token('BANG_EQUAL')
            else:
                self.add_token('BANG')
        elif c == '=':
            if self.match('='):
                self.add_token('EQUAL_EQUAL')
            else:
                self.add_token('EQUAL')
        elif c == '<':
            if self.match('='):
                self.add_token('LESS_EQUAL')
            else:
                self.add_token('LESS')
        elif c == '>':
            if self.match('='):
                self.add_token('GREATER_EQUAL')
            else:
                self.add_token('GREATER')
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token('SLASH')
        elif c in (' ', '\r', '\t'):
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()

        elif c.isalpha() or c == '_':
            self.identifier()
        else:
            from nelox import Nelox
            Nelox.error(self.line, "Unexpected character!")

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            Nelox.error(self.line, "Unterminated string.")
            return

        self.advance()

        value = self.source[self.start + 1: self.current - 1]
        self.add_token('STRING', value)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        text = self.source[self.start:self.current]
        self.add_token('NUMBER', float(text))

    def identifier(self):
        while is_alpha_numeric:
            self.advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text)
        if token_type is None:
            token_type = 'IDENTIFIER'
        self.add_token(token_type)
