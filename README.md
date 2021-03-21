# pyrepl

pyrepl allows modifying the default python REPL and makes your python experience better than ever.
It is currently in the very (very) early stages of release so expect breaking changes.

## Installation

pyrepl can be installed through pip with:
`pip install git+https://github.com/YodaPY/pyrepl.git`

Note that pyrepl was only tested on python 3.9.1 which means backwards compatibility is not ensured.

## Configuration

In order to configure pyrepl, you will have to put your configuration files into `~/.config/pyrepl`. pyrepl will parse all config files with the file extension `.pyr`.
pyrepl **won't** look for config files in subdirectories.

The following variables are supported:
  - `primary_prefix`: The primary prefix. Defaults to `>>>`. For the sake of proper indentation, it is recommended that the length of the primary prefix matches the length of the secondary prefix.
  - `primary_color`: A 6-digit hex code specifying the color of the primary prefix. Defaults to the default terminal color.
  - `secondary_prefix`: The secondary prefix, used in multi-line statements. Defaults to `...`.
  - `secondary_color`: A 6-digit hex code specifying the color of the secondary prefix. Defaults to the default terminal color.
  - `spaces`: An integer specifying the amount of padding between the prefix and the input. Defaults to `1`.
  - `startup_version`: Whether the system version should be printed out on startup. Defaults to `False`.
  - `startup_function_*`: Call a function on the startup, the value should be an importable module inside `~/.config/pyrepl`. `*` should be a function inside that module. The function must take no arguments (!).
  
## Starting the REPL

Run `python -im pyrepl.repl` to start the REPL.
