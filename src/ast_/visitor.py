from ast_.expression import Unary
from ast_.expression import Grouping
from interpreter import TokenType
from ast_.expression import *
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
class AstPrinter(ExprVisitor):
    def accept(self):
        print("This was called wtf?")
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

expr = Binary(
    Unary(Token(TokenType.MINUS, "-", None, -1),Literal(123)),
    Token(TokenType.STAR, "*", None, -1),
    Grouping(Binary(Literal(5),Token(TokenType.PLUS,"+",None,-1),Literal(3))),
)
printer = AstPrinter()
print(printer.print(expr))
