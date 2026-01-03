import unittest
from keyboard_color_controller.devices import hex_to_rgb, get_rgb
from openrgb.utils import RGBColor

class TestDevices(unittest.TestCase):
    def test_hex_to_rgb(self):
        self.assertEqual(hex_to_rgb("#FF0000"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("00FF00"), (0, 255, 0))
        self.assertEqual(hex_to_rgb("#00F"), (0, 0, 255))
        self.assertEqual(hex_to_rgb("invalid"), None)

    def test_get_rgb(self):
        # Named color
        self.assertEqual(get_rgb("red"), RGBColor(255, 0, 0))
        # Hex color
        self.assertEqual(get_rgb("#00FF00"), RGBColor(0, 255, 0))
        # Fallback
        self.assertEqual(get_rgb("unknown"), RGBColor(255, 255, 255))

if __name__ == '__main__':
    unittest.main()
