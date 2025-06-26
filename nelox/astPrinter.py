from typing import Any


class AstPrinter:
    def __init__(self):
        self.name = None

    def print_expr(self, expr):
        return expr.accept(self)

    def print_stmt(self, stmt):
        return stmt.accept(self)

    def visit_expression_stmt(self, stmt):
        return self.postfix(";", stmt.expression)

    def visit_function_stmt(self, stmt):
        parts = [b.accept(self) for b in stmt.body]
        parts.extend(p.lexeme for p in stmt.params)
        parts.append(stmt.name.lexeme)
        return f"( {' '.join(parts)} fun )"

    def visit_if_stmt(self, stmt):
        if stmt.else_branch is None:
            return self.postfix("if", stmt.then_branch, stmt.condition)
        return self.postfix("if-else", stmt.else_branch, stmt.then_branch, stmt.condition)

    def visit_print_stmt(self, stmt):
        return self.postfix("print", stmt.expression)

    def visit_return_stmt(self, stmt):
        if stmt.value is None:
            return "( return )"
        return self.postfix("return", stmt.value)

    def visit_while_stmt(self, stmt):
        return self.postfix("while", stmt.body, stmt.condition)

    def visit_assign_expr(self, expr):
        return self.postfix("=", expr.value, expr.name.lexeme)

    def visit_binary_expr(self, expr):
        return self.postfix(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr):
        return self.postfix("call", expr.arguments, expr.callee)

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_logical_expr(self, expr):
        return self.postfix(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary_expr(self, expr):
        return self.postfix(expr.operator.lexeme, expr.right)

    def visit_variable_expr(expr):
        return expr.name.lexeme

    def postfix(self, name: str, *parts: Any) -> str:
        flat = []
        for part in parts:
            flat.append(self.stringify(part))
        return f"( {' '.join(flat)} {name} )"

    def stringify(self, part: Any) -> str:
        if isinstance(part, list):
            return ' '.join(self.stringify(p) for p in part)
        elif hasattr(part, 'accept'):
            return part.accept(self)
        elif hasattr(part, 'lexeme'):
            return part.lexeme
        else:
            return str(part)
