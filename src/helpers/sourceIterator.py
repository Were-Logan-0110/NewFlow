from interpreter import Token,TokenType
from dataclasses import dataclass
from typing import Final,Union


# Character Iterator
@dataclass
class SourceIterator:
    source: Final[Union[str, list[Token]]]

    # States
    current: int = 0
    line: int = 0

    def isAtEnd(self) -> bool:
        if isinstance(self.source, str):
            return self.current >= len(self.source)
        return (
            self.current >= len(self.source)
            or self.source[self.current].type == TokenType.EOF
        )

    def advance(self) -> Union[str, Token]:
        self.current += 1
        if isinstance(self.source, str):
            return self.source[self.current - 1]
        return self.previous()

    def match(self, *toMatch: Union[str, TokenType]) -> bool:
        if isinstance(self.source, str):
            if self.isAtEnd():
                return False
            if self._getCurrent() != toMatch[0]:
                return False
            self.current += 1
            return True
        else:
            for type in toMatch:
                if self.check(type):  # type: ignore
                    self.advance()
                    return True
            return False

    def check(self, type: TokenType) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == type # type: ignore

    def _getCurrent(self) -> Union[str, Token]:
        return self.source[self.current]

    def peek(self) -> Union[str, Token]:
        if self.isAtEnd():
            if isinstance(self.source, str):
                return "\0"
            return Token(TokenType.EOF, "\0", None, -1)
        return self._getCurrent()

    def peekNext(self) -> Union[str, Token]:
        if self.isAtEnd():
            if isinstance(self.source, str):
                return "\0"
            return Token(TokenType.EOF, "\0", None, -1)
        return self.source[self.current + 1]

    def previous(self) -> Token:
        if isinstance(self.source, str):
            raise Exception("Previous is not supported for source strings")
        return self.source[self.current - 1]
