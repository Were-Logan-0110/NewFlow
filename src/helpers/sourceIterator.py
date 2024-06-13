from dataclasses import dataclass
from typing import Final

# Character Iterator
@dataclass
class SourceIterator(str):
    source: Final[str]

    # States
    start: int = 0
    current: int = 0
    line: int = 0
    def isAtEnd(self) -> bool:
        return self.current >= self.source.__len__()
    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]
    def match(self,toMatch:str) -> bool:
        # Not a match if its at the end
        if self.isAtEnd(): return False
        # Check if current character is equal to the target
        if self._getCurrent() != toMatch: return False
        # Advance
        self.current += 1
        return True
    def _getCurrent(self):
        return self.source[self.current]
    def peek(self) -> str:
        if self.isAtEnd(): return "\0"
        return self._getCurrent()
    def peekNext(self) -> str:
        if self.isAtEnd(): return "\0"
        return self.source[self.current + 1]