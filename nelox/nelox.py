import sys

from nelox.interpreter import Interpreter
from parser import Parser
from resolver import Resolver
from scanner import Scanner


class Nelox:
    interpreter = Interpreter()
    had_error = False
    had_runtime_error = False

    @classmethod
    def main(cls, args):
        if len(args) > 1:
            print("Usage: pynelox [script]")
            sys.exit(64)
        elif len(args) == 1:
            cls.run_file(args[0])
        else:
            cls.run_prompt()

    @classmethod
    def run_file(cls, path):
        with open(path, 'rb') as f:
            bytes_content = f.read()
        cls.run(bytes_content.decode())
        if cls.had_error:
            sys.exit(65)
        if cls.had_runtime_error:
            sys.exit(70)

    @classmethod
    def run_prompt(cls):
        while True:
            try:
                line = input("> ")
                cls.run(line)
                cls.had_error = False
            except EOFError:
                break

    @classmethod
    def run(cls, source):

        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        statements = parser.parse()

        if cls.had_error:
            return

        resolver = Resolver()
        resolver.resolve(statements)

        if cls.had_error:
            return

        cls.interpreter.interpret(statements)

    @classmethod
    def error(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        cls.had_error = True

    @classmethod
    def token_error(cls, token, message: str):
        if token.type == 'EOF':
            cls.report(token.line, " at end", message)
        else:
            cls.report(token.line, f" at '{token.lexeme}'", message)

    @classmethod
    def runtime_error(cls, error):
        print(f"{error}\n[line {error.token.line}]", file=sys.stderr)
        cls.had_runtime_error = True
