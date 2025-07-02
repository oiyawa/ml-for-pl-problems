import sys

from interpreter import Interpreter
from parser import Parser
from scanner import Scanner


class ParseError(Exception):
    pass


class RuntimeErrorWithToken(Exception):
    def __init__(self, message, token):
        super().__init__(message)
        self.token = token


class Nelox:
    interpreter = Interpreter()

    @classmethod
    def main(cls, args):
        if len(args) > 1:
            raise ValueError("Usage: pynelox [script]")
        elif len(args) == 1:
            cls.run_file(args[0])
        else:
            cls.run_prompt()

    @classmethod
    def run_file(cls, path):
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
        cls.run(source)

    @classmethod
    def run_prompt(cls):
        while True:
            try:
                line = input("> ")
                cls.run(line)
            except EOFError:
                break
            except Exception as e:
                print(f"[REPL Error] {e}", file=sys.stderr)

    @classmethod
    def run(cls, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        statements = parser.parse()

        if statements is None:
            raise ParseError("Parsing failed.")

        cls.interpreter.interpret(statements)

    @classmethod
    def error(cls, line: int, message: str):
        raise ParseError(f"[line {line}] Error: {message}")

    @classmethod
    def token_error(cls, token, message: str):
        if token.type == 'EOF':
            raise ParseError(f"[line {token.line}] Error at end: {message}")
        else:
            raise ParseError(f"[line {token.line}] Error at '{token.lexeme}': {message}")

    @classmethod
    def runtime_error(cls, error):
        raise RuntimeErrorWithToken(f"{error}", error.token)
