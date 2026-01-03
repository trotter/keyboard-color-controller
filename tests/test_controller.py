import unittest
from unittest.mock import MagicMock
from keyboard_color_controller.controller import Controller
from keyboard_color_controller.layout import LAYOUT

class TestController(unittest.TestCase):
    def test_set_ascii_art(self):
        mock_device = MagicMock()
        controller = Controller(mock_device)
        
        art = " X \nXXX"
        fg = "red"
        bg = "black"
        
        controller.set_ascii_art(art, fg, bg)
        
        # Check some calls
        # Row 0: " X "
        # Esc (0,0) -> ' ' -> bg
        # F1 (0,1) -> 'X' -> fg
        # F2 (0,2) -> ' ' -> bg
        # F3 (0,3) -> past line -> bg
        
        mock_device.set_key_color.assert_any_call('Esc', bg)
        mock_device.set_key_color.assert_any_call('F1', fg)
        mock_device.set_key_color.assert_any_call('F2', bg)
        mock_device.set_key_color.assert_any_call('F3', bg)
        
        # Row 1: "XXX"
        # ` (1,0) -> 'X' -> fg
        # 1 (1,1) -> 'X' -> fg
        # 2 (1,2) -> 'X' -> fg
        # 3 (1,3) -> past line -> bg
        
        mock_device.set_key_color.assert_any_call('`', fg)
        mock_device.set_key_color.assert_any_call('1', fg)
        mock_device.set_key_color.assert_any_call('2', fg)
        mock_device.set_key_color.assert_any_call('3', bg)
        
        # Row 2+: all bg
        mock_device.set_key_color.assert_any_call('Tab', bg)

if __name__ == '__main__':
    unittest.main()
