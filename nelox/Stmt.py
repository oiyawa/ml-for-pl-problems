class Stmt:
    def accept(self, visitor):
        raise NotImplementedError()


class StmtVisitor:
    def visit_Expression_Stmt(self, stmt):
        pass

    def visit_Function_Stmt(self, stmt):
        pass

    def visit_If_Stmt(self, stmt):
        pass

    def visit_Print_Stmt(self, stmt):
        pass

    def visit_Return_Stmt(self, stmt):
        pass

    def visit_While_Stmt(self, stmt):
        pass


class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_Expression_Stmt(self)


class Function(Stmt):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_Function_Stmt(self)


class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_If_Stmt(self)


class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_Print_Stmt(self)


class Return(Stmt):
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_Return_Stmt(self)


class While(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_While_Stmt(self)
