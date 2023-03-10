""" Checks for available hotkeys on Windows systems

Currently only able to check for all hotkeys and list them. Supports keys (a-z,
0-9, numpad 0-9, tab, function 1-16, tab, backspace and arrow keys) and
modifier keys (ctrl, alt, shift).

Windows registered default hotkeys allow being overwritten, so this script will
not be able to detect them. For example ctrl + c the default hotkey for copy,
but it can be overwritten.

This script only detects hotkeys that unavailable to be registered because they
have already been registered by another program.

Only works on Windows systems. Tested on Window 7, 10, and 11.

"""
__all__ = ["list_used_hotkeys"]


import argparse
import ctypes
import itertools
import os
import sys


def hotkey_is_available(mods: int, vkey: int) -> bool:
  """ Returns True if the hotkey is available, False otherwise
  
  It checks by literally registering the hotkey and then unregistering it. If
  Windows allows it, the hotkey is available. If it doesn't, it's already being
  used by another program.
  """
  hotkey_available = False
  try:
    if ctypes.windll.user32.RegisterHotKey(None, 1, mods, vkey):
      hotkey_available = True
  except:  #pylint: disable=bare-except
    pass
  finally:
    ctypes.windll.user32.UnregisterHotKey(None, 1)
  return hotkey_available


def generate_all_modifier_combos(basic_modifiers: dict[str, int]) -> list[int]:
  """ Returns a list of int codes for modifier combinations """
  mod_codes = []
  for n in range(1, len(basic_modifiers.values())+1):
    for mods in itertools.combinations(basic_modifiers.values(), n):
      mod = mods[0]
      for m in mods:
        mod = mod | m
      mod_codes.append(mod)
  return mod_codes


def to_readable_modifier_keys(
    modifier: int, modifier_map: dict[str, int]) -> list[str]:
  """ Converts a modifier int code to a list of readable modifier names """
  text_modifiers = []
  for key, value in modifier_map.items():
    if value & modifier == value:
      text_modifiers.append(key)
  return text_modifiers


def get_vkey_code_map() -> dict[int, str]:
  """" Returns a map of virtual key codes to readable names"""
  # Digits and numbers
  key_map = {}
  for i in range(0, 10):
    key_map[ord(str(i))] = i
  for i in range(ord('A'), ord('Z')+1):
    key_map[i] = chr(i+32)
  # Special keys
  key_map[8] = "tab"
  key_map[9] = "backspace"
  key_map[37] = "left"
  key_map[38] = "up"
  key_map[39] = "right"
  key_map[40] = "down"
  # Numpad
  key_map[106] = "numpad_mult"
  key_map[107] = "numpad_add"
  key_map[108] = "numpad_separator"
  key_map[109] = "numpad_subtract"
  key_map[110] = "numpad_decimal"
  key_map[111] = "numpad_divide"
  for i in range(96, 106):
    n = i - 96
    key_map[i] = f"numpad{n}"
  # F keys
  for i in range(112, 128):
    n = i - 112 + 1
    key_map[i] = f"f{n}"
  return key_map


def get_modifier_map() -> dict[str, int]:
  """ Return a map of modifier names to their virtual key codes """
  kNO_REPEAT = 0x4000
  return {
    "ctrl": 0x0002 | kNO_REPEAT,
    "alt": 0x0001 | kNO_REPEAT,
    "shift": 0x0004 | kNO_REPEAT,
  }


def modifier_code_and_vkey_to_readable(
    mod_code: int, modifier_map: dict[str, int],
    vkey: int, vkey_map: dict[int, str]) -> str:
  """ Converts a modifier code and virtual key code to a readable string """
  s = " + ".join(
    [x for x in to_readable_modifier_keys(mod_code, modifier_map)])
  return f"{s}, {vkey_map[vkey]}"


def list_used_hotkeys() -> list[str]:
  """ Return a list of readable hotkeys that are in use """
  # Get all available normal keys
  vkeys_map = get_vkey_code_map()
  # Get all available modifiers
  modifier_map = get_modifier_map()
  # and all possible modifier combinations
  mod_list = generate_all_modifier_combos(modifier_map)
  # Brute force check all possible combinations
  valid_hotkeys = []
  invalid_hotkeys = []
  for mods in mod_list:
    for vkey in vkeys_map:
      if hotkey_is_available(mods, vkey):
        valid_hotkeys.append((mods, vkey))
      else:
        invalid_hotkeys.append((mods, vkey))
  if not invalid_hotkeys:
    return []
  return [modifier_code_and_vkey_to_readable(
    mods, modifier_map, vkey, vkeys_map) for mods, vkey in invalid_hotkeys]

def main():
  # Check that the script is being run on Windows
  if os.name != "nt":
    print("This script is only compatible with Windows systems.")
    return 1

  parser = argparse.ArgumentParser(description=__doc__)
  parser.parse_args()
  # List all used hotkeys and exit:
  hotkey_list = list_used_hotkeys()
  if not hotkey_list:
    print("Found no hotkeys are registered to another program.")
    return 0
  print("The following hotkeys are registered to another program:")
  for hk in hotkey_list:
    print(hk)


if __name__ == "__main__":
  sys.exit(main())