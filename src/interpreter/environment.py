from interpreter.tokens import Token
from dataclasses import dataclass
from typing import Final

class __:
    pass

@dataclass
class Environment:
    values: Final[dict[str,object]]
    enclosing: Final["Environment | None"] = None
    def define(self,name: str,value: object):
        if self.enclosing:
            self.enclosing.define(name,value)
            return
        self.values[name] = value
    def get(self,name: Token) -> object:
        val = (
            self.values.get(name.lexeme, __())
            if not self.enclosing
            else self.enclosing.get(name)
        )
        if not isinstance(val, __):
            return val
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")
