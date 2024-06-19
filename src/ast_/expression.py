from dataclasses import dataclass,field
from interpreter import Token,error
from abc import ABC,abstractmethod
from numpy import ndarray
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
class Array(Expr):
    elements: ndarray[Expr]
    def accept(self,visitor):
        return visitor.visitArrayExpr(self)
@dataclass
class Index(Expr):
    collection: Expr
    index: Expr


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)

@dataclass
class Variable(Expr):
    name: Final[Token]
    def accept(self, visitor) -> None:
        return visitor.visitVariableExpr(self)
class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass
@dataclass
class Expression(Stmt):
    expression: Expr
    def accept(self, visitor) -> None:
        return visitor.visitExpressionStmt(self)
@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr
    def accept(self,visitor):
        return visitor.visitVarStmt(self)
@dataclass
class Block(Stmt):
    statements: list[Stmt]
    stmtBlock: bool = False
    def accept(self,visitor):
        return visitor.visitBlockStmt(self)


@dataclass
class If(Stmt):
    condition: Expr
    thenBranch: Stmt
    elseIfs: "list[If]" = field(default_factory=[]) # type: ignore
    elseBranch: Stmt | None = None
    def accept(self,visitor):
        return visitor.visitIfStmt(self)
@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt
    def accept(self, visitor):
        return visitor.visitWhileStmt(self)
@dataclass
class For(Stmt):
    initializer: Expression 
@dataclass
class Foreach(Stmt):
    collections: Array
    body: Stmt
    variable: Variable | None = None
    def accept(self,visitor):
        return visitor.visitForeachStmt(self)
@dataclass
class Break(Stmt):
    def accept(self,visitor):
        return visitor.visitBreakStmt(self)
@dataclass
class Continue(Stmt):
    def accept(self,visitor):
        return visitor.visitContinueStmt(self)
@dataclass
class Print(Expression):
    newLine: bool = False
    def accept(self, visitor):
        return visitor.visitPrintStmt(self)