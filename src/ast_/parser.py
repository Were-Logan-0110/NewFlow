from ast_ import Expr, Binary, Unary, Literal, Grouping, Stmt, Print, Expression, Var,Variable,Block,If
from interpreter import Token, TokenType, report, error
from dataclasses import dataclass, field
from helpers import SourceIterator


class ParseError(Exception):
    pass

class _UninitializedVar:
    pass
@dataclass
class LLParser(SourceIterator):
    tokens: list[Token] = field(default_factory=lambda: [])

    def parse(self) -> list[Stmt | None]:
        try:
            statements: list[Stmt | None] = []
            while not self.isAtEnd():
                statements.append(self.declaration())
            return statements
        except ParseError as e:
            exit(1)

    def declaration(self) -> Stmt | None:
        try:
            if self.match(TokenType.IDENTIFIER):
                return self.varDeclaration()
            return self.statement()
        except ParseError as e:
            self.sync()
            return None

    def statement(self) -> Stmt:
        if self.match(TokenType.IF): return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.PRINTLN):
            return self.printStatement(True)
        if self.match(TokenType.LEFT_BRACE):
            return self.block()
        return self.expressionStatement()
    def block(self) -> Stmt:
        statements: list[Stmt | None] = []
        while (not self.check(TokenType.RIGHT_BRACE)) and (not self.isAtEnd()):
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return Block(statements) # type: ignore
    def ifStatement(self) -> Stmt:
        # self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition: Expr = self.expression()
        self.consume(TokenType.COLON, "Expect ':' after 'if'.")
        thenBranch = self.statement()
        elseIfs: list[If] = []
        elseBranch = None
        while self.match(TokenType.ELSE_IF):
            _condition: Expr = self.expression()
            self.consume(TokenType.COLON, "Expect ':' after 'if'.")
            _thenBranch = self.statement()
            elseIfs.append(If(_condition,_thenBranch,[],None))
        if self.match(TokenType.ELSE):
            self.consume(TokenType.COLON, "Expect ':' after 'else'.")
            elseBranch = self.statement()
        return If(condition,thenBranch,elseIfs,elseBranch)
    def varDeclaration(self):
        name: Token = self.previous()
        initializer: Expr | None | _UninitializedVar = _UninitializedVar()
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)  # type: ignore

    def printStatement(self, newLine: bool = False) -> Stmt:
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value, newLine)

    def expressionStatement(self):
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr: Expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()
        while self.match(
            TokenType.AND,
            TokenType.OR,
            TokenType.XOR,
            TokenType.R_SHIFT,
            TokenType.L_SHIFT,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Unary(operator, right)
            return expr
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NULL):
            return Literal(None)
        if self.match(TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return self.variable()
        if self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN,
                "Expected Enclosing parentheses ')' after expression.'",
            )
            return Grouping(expr)
        raise self.error(self.peek(), "Expect expression.")  # type: ignore

    def variable(self) -> Expr:
        name = self.previous()
        if self.match(TokenType.EQUAL):
            value = self.expression()
            return Var(name, value) # type: ignore
        return Variable(name)
    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()  # type: ignore
        raise self.error(self.peek(), message)  # type: ignore

    def error(self, token: Token, message: str) -> ParseError:
        self.tokenError(token, message)
        return ParseError()

    def tokenError(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            report(token.line, " at end", message)
        else:
            report(token.line, " at '" + token.lexeme + "'", message)
        exit(1)

    def sync(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return
            match self.peek().type:  # type: ignore
                case TokenType.FUN:
                    return
                case TokenType.FOR:
                    return
                case TokenType.IF:
                    return
                case TokenType.WHILE:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.PRINTLN:
                    return
                case TokenType.RETURN:
                    return
                case TokenType.HTTP:
                    return
                case TokenType.FTP:
                    return
                case TokenType.STMP:
                    return
                case TokenType.TCP:
                    return
                case TokenType.IP:
                    return
                case TokenType.SSL:
                    return
                case TokenType.TYPE_INTEGER:
                    return
                case TokenType.TYPE_FLOAT:
                    return
                case TokenType.TYPE_BOOLEN:
                    return
                case TokenType.TYPE_STRING:
                    return
