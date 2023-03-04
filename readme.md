# Windows Hotkey Checker
## Simple CL tool to check for registered hotkeys on Windows

This is a simple python script that checks for hotkeys that already regitstered
by other programs on Windos and prints them to the console.

It works by enumerating combinations of modifiers and keys and trying to
register them as new hotkeys. If the registration fails, it means that the
combination is already registered by another program.

## Installation

The script can be installed with pip:

    pip install windows_hotkey_checker

and only uses python standard library modules, so no additional dependencies.

## Usage

Usage is simple. Just run the script with python:

    > python -m windows_hotkey_checker

There is also a Script installed in the Scripts directory of the python with
the short name of "hotkeys" that you can run from the command line as:
  
      > hotkeys