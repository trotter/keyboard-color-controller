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
        mock_device.set_key_color.assert_any_call('Esc', bg)
        mock_device.set_key_color.assert_any_call('F1', fg)
        
    def test_set_color_hex(self):
        mock_device = MagicMock()
        controller = Controller(mock_device)
        
        controller.set_color("#FF00FF")
        mock_device.set_color.assert_called_with("#FF00FF")

if __name__ == '__main__':
    unittest.main()
