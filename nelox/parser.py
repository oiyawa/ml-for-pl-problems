from nelox.nelox_token import Token
from nelox.tokenType import TokenType
from nelox.Expr import Literal, Variable, Call, Binary, Unary, IfExpr, Set


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        expressions = []
        while not self.is_at_end():
            expressions.append(self.expression())
        return expressions

    def expression(self):
        if self.match(TokenType.LEFT_PAREN):
            return self.list_expr()
        elif self.match(TokenType.NUMBER, TokenType.STRING, TokenType.TRUE, TokenType.FALSE):
            return Literal(self.previous().literal)
        elif self.match(TokenType.IDENTIFIER, TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH):
            return Variable(self.previous())
        else:
            raise Exception(f"Unexpected token: {self.peek().type}")

    def list_expr(self):
        if self.check(TokenType.RIGHT_PAREN):
            self.advance()
            return Literal([])

        callee = self.expression()

        args = []
        while not self.check(TokenType.RIGHT_PAREN) and not self.is_at_end():
            args.append(self.expression())

        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after list.")

        if isinstance(callee, Variable) and callee.name.lexeme in ('+', '-', '*', '/'):
            op = callee.name
            if len(args) == 2:
                return Binary(args[0], op, args[1])
            elif op.lexeme == '-' and len(args) == 1:
                return Unary(op, args[0])
            else:
                raise Exception(f"Operator '{op.lexeme}' expects 1 or 2 arguments")

        if isinstance(callee, Variable) and callee.name.lexeme == 'if':
            if len(args) != 3:
                raise Exception("if expects 3 arguments: (if condition then else)")
            return IfExpr(args[0], args[1], args[2])

        if isinstance(callee, Variable) and callee.name.lexeme == 'define':
            if len(args) != 2:
                raise Exception("define expects 2 arguments: (define name value)")
            if not isinstance(args[0], Variable):
                raise Exception("First argument to define must be a variable")
            return Set(args[0], args[1])

        return Call(callee, paren, args)

    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise Exception(f"[line {self.peek().line}] Error: {message}")

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
