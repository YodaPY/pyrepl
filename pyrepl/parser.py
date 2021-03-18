import re
from .lexer import Lexer, Token
from typing import Any, Dict, Optional, Final
from difflib import get_close_matches

def ansi(hex_code) -> str:
    if re.match(r"^[\dA-Za-z]{6}$", hex_code):
        hex_code = int(hex_code, 16)
        r, g, b = (hex_code >> 16, (hex_code >> 8) % 256, hex_code % 256)
        return f"\33[38;2;{r};{g};{b}m"

    raise ValueError

UNEXPECTED_TOKEN = "Unexpected token {value} at line {lineno}, column {column}"
UNEXPECTED_VARIABLE = "Unexpected variable {value} at line {lineno}, column {column}{vars_message}"
UNEXPECTED_TYPE = "Unexpected type of value {value} at line {lineno}, column {column}"
VALID_VARS: Final[Dict[str, Any]] = {
    "prefix": str,
    "spaces": int,
    "color": ansi
}

def get_close_vars(var: str, /) -> Optional[str]:
    matches = get_close_matches(var, VALID_VARS)
    if matches:
        matches = [repr(match) for match in matches]
        if len(matches) > 1:
            s = ". Perhaps you meant " + ", ".join(matches[:-1]) + f" or {matches[-1]}"

        else:
            s = f". Perhaps you meant {matches[0]}"

        return s

class ParsingError(Exception):
    def __init__(self, token: Token, message: str, /):
        self.token = token
        self.message = message

class Parser:
    def __init__(self, *, lexer: Lexer) -> None:
        self.lexer = lexer
        self.token: Token = self.lexer.next_token()
        self.globals: Dict[str, str] = {}

    def eat(self, token_type, /) -> None:
        if self.token.type == token_type:
            self.token = self.lexer.next_token()

        else:
            error = UNEXPECTED_TOKEN.format(
                value=repr(self.token.value),
                lineno=self.token.lineno,
                column=self.token.column
            )
            raise ParsingError(self.token, error)

    def parse(self) -> None:
        while self.token.type != "EOF":
            token = self.token
            name = token.value
            self.eat("ID")
            if name not in VALID_VARS:
                close_vars = get_close_vars(name) or ""
                error = UNEXPECTED_VARIABLE.format(
                    value=repr(token.value),
                    lineno=token.lineno,
                    column=token.column,
                    vars_message=close_vars
                )
                raise ParsingError(token, error)
            
            self.eat("ASSIGN")
            value = self.token.value
            self.eat("ID")

            try:
                value = VALID_VARS[name](value)

            except ValueError:
                error = UNEXPECTED_TYPE.format(
                    value=repr(value),
                    lineno=token.lineno,
                    column=token.column
                )

                raise ParsingError(token, error)

            else:
                self.globals[name] = value