from interpreter import Token,error
from dataclasses import dataclass
from abc import ABC,abstractmethod
from typing import Final
class Expr(ABC):
    @abstractmethod
    def accept(self,visitor):
        error(-1,f"No Accept Method Found For Object: <{self.__class__}>")
        exit(1)
@dataclass
class Binary(Expr):
    left: Final[Expr]
    operator: Final[Token]
    right: Final[Expr]
    def accept(self,visitor):
        return visitor.visitBinaryExpr(self)


@dataclass
class Grouping(Expr):
    expression: Expr
    def accept(self,visitor):
        return visitor.visitGroupExpr(self)


@dataclass
class Literal(Expr):
    value: object
    def accept(self,visitor):
        return visitor.visitLiteralExpr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)
