import os
import sys
import glob
from .lexer import Lexer
from .parser import Parser
from .utils import config

config_vars = {
    "primary_prefix": ">>>",
    "primary_color": None,
    "secondary_prefix": "...",
    "secondary_color": None,
    "spaces": 1,
    "startup_version": False
}

def parse_config_files() -> None:
    config_path = config.get_config_path()
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
    primary_prefix = config_vars["primary_prefix"] + prefix_pad
    secondary_prefix = config_vars["secondary_prefix"] + prefix_pad
    
    if config_vars["primary_color"]:
        primary_prefix = config_vars["primary_color"] + primary_prefix + "\33[39m"

    if config_vars["secondary_color"]:
        secondary_prefix = config_vars["secondary_color"] + secondary_prefix + "\33[39m"

    sys.ps1 = primary_prefix
    sys.ps2 = secondary_prefix

    if config_vars["startup_version"]:
        print(sys.version)

    functions = [config_vars[name] for name in config_vars if name.startswith("startup_function_")]
    for function in functions:
        function()

if __name__ == "__main__":
    parse_config_files()
    update_repl()