from interpreter import TokenType,report,Environment
from ast_.expression import Binary, Literal, Stmt
from ast_.expression import Grouping
from ast_.expression import Unary
from numpy import ndarray,array
from ast_.expression import *
from copy import deepcopy
class ExprVisitor(Expr):
    @abstractmethod
    def visitBinaryExpr(self,expr:Binary):
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal):
        pass

    @abstractmethod
    def visitUnaryExpr(self,expr:Unary):
        pass

    @abstractmethod
    def visitGroupExpr(self,expr:Grouping):
        pass
class StmtVisitor(Expr):
    @abstractmethod
    def visitExpressionStmt(self,expr:Stmt):
        pass
    @abstractmethod
    def visitPrintStmt(self,expr:Stmt):
        pass
class AstPrinter(ExprVisitor):
    def accept(self):
        pass
    def print(self,expr:Expr) -> str:
        return expr.accept(self)
    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme,expr.left,expr.right)
    def visitGroupExpr(self, expr: Grouping):
        return self.parenthesize("group",expr.expression)
    def visitLiteralExpr(self, expr: Literal):
        return str(expr.value)
    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(f"{expr.operator.lexeme} {expr.right.accept(self)}")
    def parenthesize(self,name:str,*args:Expr):
        return f"({name} {' '.join([expr.accept(self) for expr in args])})"

class AstRPN(ExprVisitor):
    def accept(self):
        pass
    def print(self,expr:Expr) -> str:
        return expr.accept(self)
    def visitBinaryExpr(self, expr: Binary):
        return f"{expr.left.accept(self)} {expr.right.accept(self)} {expr.operator.lexeme}"
    def visitGroupExpr(self, expr: Grouping):
        return expr.expression.accept(self)
    def visitLiteralExpr(self, expr: Literal):
        return str(expr.value)
    def visitUnaryExpr(self, expr: Unary):
        return f"{expr.operator.lexeme}{expr.right.accept(self)}"
    def parenthesize(self,name:str,*args:Expr):
        return f"({name} {' '.join([expr.accept(self) for expr in args])})"
class ASTInterpreter(ExprVisitor,StmtVisitor):
    environment: Environment = Environment({})
    def accept(self, visitor):
        return super().accept(visitor)
    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except Exception as e:
            raise RuntimeError(e)
    def execute(self,statement: Stmt):
        statement.accept(self)
    def visitBlockStmt(self,stmt: Block):
        self.executeBlock(stmt.statements,Environment({},self.environment))
    def visitExpressionStmt(self,stmt: Expression):
        self.evaluate(stmt.expression)
    def visitPrintStmt(self, expr: Print):
        value: object = self.evaluate(expr.expression)
        if isinstance(value,None.__class__):
            value = 'nil'
        print(value,end=('\n' if expr.newLine else ''))        
    def visitLiteralExpr(self, expr: Literal) -> object:
        return expr.value
    def visitGroupExpr(self, expr: Grouping):
        return self.evaluate(expr.expression)
    def visitUnaryExpr(self, expr: Unary) -> object:
        right: object = self.evaluate(expr.right)
        expr.right
        match expr.operator.type:
            case TokenType.MINUS:
                return -right  # type: ignore
            case TokenType.BANG:
                return not self.isTruthy(right)
        return None
    def visitBinaryExpr(self, expr: Binary):
        right: object = self.evaluate(expr.right)
        left: object = self.evaluate(expr.left)
        try:
            match expr.operator.type:
                case TokenType.MINUS:
                    return left - right  # type: ignore
                case TokenType.PLUS:
                    return left + right # type: ignore
                case TokenType.SLASH:
                    return left / right  # type: ignore
                case TokenType.STAR:
                    return left * right # type: ignore
                case TokenType.AND:
                    return left & right # type: ignore
                case TokenType.OR:
                    return left | right # type: ignore
                case TokenType.XOR:
                    return left & right  # type: ignore
                case TokenType.L_SHIFT:
                    return left << right  # type: ignore
                case TokenType.R_SHIFT:
                    return left >> right  # type: ignore
                case TokenType.GREATER:
                    return left > right  # type: ignore
                case TokenType.GREATER_EQUAL:
                    return left >= right # type: ignore
                case TokenType.LESS:
                    return left < right # type: ignore
                case TokenType.LESS_EQUAL:
                    return left <= right # type: ignore
                case TokenType.BANG_EQUAL:
                    return not self.isEqual(left, right)
                case TokenType.EQUAL_EQUAL:
                    return self.isEqual(left,right)
        except Exception as e:
            report(
                expr.operator.line,
                "",
                f" unsupported operand type(s) for {expr.operator.lexeme}: '{left.__class__.__name__}' and '{right.__class__.__name__}' ",
            )
        return None
    def visitVarStmt(self,stmt: Var):
        value: object = None
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme,value)
    def visitVariableExpr(self,stmt: Variable):
        return self.environment.get(stmt.name)
    def visitIfStmt(self,stmt: If):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseIfs:
            for _elif in stmt.elseIfs:
                if self.isTruthy(self.evaluate(_elif.condition)):
                    self.execute(_elif.thenBranch)
                    return
        elif stmt.elseBranch:
            self.execute(stmt.elseBranch)
    def executeBlock(self,statements: list[Stmt],environment: Environment):
        previous: Environment = deepcopy(self.environment)
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
    def evaluate(self, expr: Expr):
        return expr.accept(self)
    def isTruthy(self,obj: object):
        return bool(obj)
    def isEqual(self,left: object,right: object):
        return left == right
