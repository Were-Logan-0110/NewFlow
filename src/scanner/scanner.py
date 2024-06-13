from interpreter import Token,TokenType,error
from helpers import SourceIterator,keywords
from dataclasses import dataclass,field
@dataclass
class Scanner(SourceIterator):
    tokens: list[Token] = field(default_factory=lambda: [])
    def scan(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF,"\0",None,self.line))
        return self.tokens
    # Tokenize Source Code
    def scanToken(self) -> list[Token]:
        char = self.advance()
        match char:
            # Single Characters Tokens
            case "(":
                self.addToken(TokenType.LEFT_PAREN)
            case ')': self.addToken(TokenType.RIGHT_PAREN)
            case '{': self.addToken(TokenType.LEFT_BRACE)
            case '}': self.addToken(TokenType.RIGHT_BRACE)
            case ',': self.addToken(TokenType.COMMA)
            case '.': self.addToken(TokenType.DOT)
            case '-': self.addToken(TokenType.MINUS)
            case '+': self.addToken(TokenType.PLUS)
            case ':': self.addToken(TokenType.COLON)
            case ';': self.addToken(TokenType.SEMICOLON)
            case '*': self.addToken(TokenType.STAR)
            case "|": self.addToken(TokenType.OR)
            case "&":
                self.addToken(TokenType.POS_ARGS if self.match("&") else TokenType.AND)
            case "!":
                self.addToken(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
            case "=":
                self.addToken(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
            case ">":
                self.addToken(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
            case "<":
                self.addToken(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and (not self.isAtEnd()): self.advance()
                else:
                    self.addToken(TokenType.SLASH)
            case " ": pass
            case "\r": pass
            case "\t": pass
            case "\n": self.line += 1
            case '"': self.parseString()
            # case "f":
            #     if self.match('"'):
            #         self.parseString(True)
            #     else:
            #         pass
            case _:
                if char.isdigit():
                    self.parseNumber()
                elif char.isalpha():
                    self.parseIdentifier()
                else:
                    error(self.line,f"Unexpected Character <{char}>.")
                    return []
        return self.tokens
    def addToken(self,tokenType:TokenType,literal: object= None) -> None:
        # Extract Lexeme
        lexeme: str = self.source[self.start:self.current]
        self.tokens.append(Token(tokenType,lexeme,literal,self.line))
    def parseString(self,formatted:bool=False) -> None:
        while (self.peek() != '"' and (not self.isAtEnd())):
            if self.peek() == "\n":
                self.line += 1
                error(self.line,"Unterminated string literal.")
                exit(1)
            self.advance()
        if (self.isAtEnd()):
            error(self.line,"Unterminated string literal.")
            exit(1)
        self.advance()
        string = self.source[self.start + 1:self.current-1]
        self.addToken(TokenType.STRING if not formatted else TokenType.FORM_STRING,string)
    def parseNumber(self) -> None:
        isFloat = False
        while self.peek().isdigit(): self.advance()
        if self.peek() == "." and self.peekNext().isdigit():
            isFloat = True
            self.advance()
            while self.peek().isdigit(): self.advance()
        self.addToken(TokenType.FLOAT if isFloat else TokenType.INTEGER,eval(self.source[self.start:self.current]))
    def parseIdentifier(self) -> None:
        while self.peek().isalnum(): self.advance()
        text = self.source[self.start:self.current]
        tokenType = keywords.get(text)
        if text == "f" and self.peek() == '"':
            self.advance()
            self.parseString(True)
            return
        if not tokenType:
            tokenType = TokenType.IDENTIFIER
        self.addToken(tokenType)