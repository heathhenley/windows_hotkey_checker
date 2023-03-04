# __main__.py
import argparse
import os
import sys

from windows_hotkey_checker import hotkeys


__doc__ = hotkeys.__doc__


def main():
  # Check that the script is being run on Windows
  if os.name != "nt":
    print("This script is only compatible with Windows systems.")
    return 1

  parser = argparse.ArgumentParser(description=__doc__)
  parser.parse_args()
  # List all used hotkeys and exit:
  hotkey_list = hotkeys.list_used_hotkeys()
  if not hotkey_list:
    print("Found no hotkeys are registered to another program.")
    return 0
  print("The following hotkeys are registered to another program:")
  for hk in hotkey_list:
    print(hk)


if __name__ == "__main__":
  sys.exit(main())