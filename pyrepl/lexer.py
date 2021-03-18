from typing import Any

class Token:
    __slots__ = ("type", "value", "lineno", "column")

    def __init__(self, type: str, value: Any, /, *, lineno: int, column: int) -> None:
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __repr__(self):
        return f"Token({self.type}: {self.value})"

def error_arrow(column: int, /, *, pad: int) -> str:
    arrow = "-" * (column - 1 + pad)
    arrow += "^"
    return arrow

INVALID_SYNTAX = "Invalid syntax at line {lineno}, column {column}\n\n{source}"
VALID_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&()*+,-./:;<>?@[\\]^_`{|}~"

class LexerError(Exception):
    def __init__(self, message, /, *, lineno: int, column: int) -> None:
        self.lineno = lineno
        self.column = column
        self.message = message

class Lexer:
    __slots__ = ("text", "pos", "char", "column", "lineno")

    def __init__(self, *, text: str) -> None:
        self.text = text
        self.pos: int = 0
        self.char: str = self.text[self.pos]
        self.column: int = 1
        self.lineno: int = 1

    def advance(self):
        if self.char == "\n":
            self.lineno += 1
            self.column = 0

        self.pos += 1
        if self.pos > (len(self.text) - 1):
            self.char = None

        else:
            self.char = self.text[self.pos]
            self.column += 1

    def skip_whitespace(self) -> None:
        while self.char and self.char.isspace():
            self.advance()

    def skip_comment(self) -> None:
        while self.char and self.char != "\n":
            self.advance()

    def _id(self):
        s = ""
        while self.char and self.char in VALID_CHARS:
            s += self.char
            self.advance()
        
        return s

    def next_token(self) -> Token:
        while self.char:
            if self.char in VALID_CHARS:
                token_id = self._id()
                return Token("ID", token_id, lineno=self.lineno, column=self.column)

            if self.char == "=":
                self.advance()
                return Token("ASSIGN", "=", lineno=self.lineno, column=self.column)

            if self.char.isspace():
                self.skip_whitespace()
                continue

            if self.char == "#":
                self.skip_comment()
                continue

            else:
                lines = self.text.splitlines()
                line = lines[self.lineno - 1]
                pad = len(str(self.lineno)) + 3 #skip spaces and |
                source = f"{self.lineno} | {line}\n{error_arrow(self.column, pad=pad)}"
                error = INVALID_SYNTAX.format(
                    lineno=self.lineno,
                    source=source,
                    column=self.column
                )

                raise LexerError(error, lineno=self.lineno, column=self.column)

        return Token("EOF", None, lineno=self.lineno, column=self.column)