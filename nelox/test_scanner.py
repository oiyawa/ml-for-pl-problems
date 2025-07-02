import unittest
from scanner import Scanner
from tokenType import TokenType


class TestScanner(unittest.TestCase):
    def test_single_parentheses(self):
        scanner = Scanner("()")
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0].type, TokenType.LEFT_PAREN)
        self.assertEqual(tokens[1].type, TokenType.RIGHT_PAREN)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_number_token(self):
        scanner = Scanner("123")
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].literal, 123.0)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_identifier_token(self):
        scanner = Scanner("print")
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0].type, TokenType.PRINT)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_unterminated_string(self):
        source = '"hello world'
        scanner = Scanner(source)
        with self.assertRaises(SyntaxError):
            scanner.scan_tokens()

    def test_simple_expression(self):
        scanner = Scanner("(add 2 3)")
        types = [t.type for t in scanner.scan_tokens()]

        expected = [
            TokenType.LEFT_PAREN,
            TokenType.IDENTIFIER,
            TokenType.NUMBER,
            TokenType.NUMBER,
            TokenType.RIGHT_PAREN,
            TokenType.EOF
        ]
        self.assertEqual(types, expected)


if __name__ == '__main__':
    unittest.main()
