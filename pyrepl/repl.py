import os
import sys
import glob
from .lexer import Lexer
from .parser import Parser

config_vars = {
    "prefix": ">>>",
    "spaces": 1
}

def parse_config_files() -> None:
    home = os.path.expanduser("~")
    config_path = os.path.join(home, ".config/pyrepl")
    config_paths = glob.glob(f"{config_path}/*.pyr")

    for path in config_paths:
        with open(path) as f:
            text = f.read()

        if not text:
            continue

        lexer = Lexer(text=text)
        parser = Parser(lexer=lexer)
        parser.parse()
        config_vars.update(parser.globals)

def update_repl() -> None:
    prefix_pad = " " * config_vars["spaces"]
    sys.ps1 = config_vars["prefix"] + prefix_pad

if __name__ == "__main__":
    parse_config_files()
    update_repl()