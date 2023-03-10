import pytest
from windows_hotkey_checker import hotkeys
from all_the_hotkeys import ALL_CURRENT_HOTKEYS

# Mock the hotkey_is_available function - it wraps the actual call to the OS
# and we don't want to actually call it.
def test_list_used_hotkeys_all_available(mocker):
    mocker.patch(
      "windows_hotkey_checker.hotkeys.hotkey_is_available", return_value=True)
    assert hotkeys.list_used_hotkeys() == []

def test_list_used_hotkeys_none_available(mocker):
    mocker.patch(
      "windows_hotkey_checker.hotkeys.hotkey_is_available", return_value=False)
    assert hotkeys.list_used_hotkeys() == ALL_CURRENT_HOTKEYS


test_mod_vkey_label = [
    (0x4002, ord('A'), 'ctrl, a'),
    (0x4002, ord('B'), 'ctrl, b'),
    (0x4002 | 0x4001, ord('Z'), 'ctrl + alt, z'),
    (0x4002 | 0x4001 | 0x4004, 110, 'ctrl + alt + shift, numpad_decimal'),
    (0x4001, 37, 'alt, left')
] 
# This test mocks the hotkey_is_available function to return False for the given
# given modifier and vkey codes. Then confirms the codes are converted to the
# expected label. 
@pytest.mark.parametrize("mods,vkey,expected", test_mod_vkey_label)
def test_list_used_hotkeys_some_used(mods, vkey, expected, mocker):
    def mock_hotkey_is_available(x, y):
      # Return True for everthing except the given mods and vkey
      return not (x == mods and y == vkey)
    mocker.patch(
      "windows_hotkey_checker.hotkeys.hotkey_is_available",
      new_callable=lambda: mock_hotkey_is_available)
    assert hotkeys.list_used_hotkeys() == [expected]