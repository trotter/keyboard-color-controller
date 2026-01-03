from .layout import LAYOUT
from .devices import Device

class Controller:
    def __init__(self, device: Device) -> None:
        self.device = device

    def set_color(self, color: str) -> None:
        """Sets the color of the entire device."""
        self.device.set_color(color)

    def set_key_color(self, key: str, color: str) -> None:
        """Sets the color of a specific key."""
        self.device.set_key_color(key, color)

    def set_ascii_art(self, art: str, fg: str, bg: str) -> None:
        """Displays ASCII art on the keyboard."""
        lines = art.splitlines()
        for r, row_keys in enumerate(LAYOUT):
            line = lines[r] if r < len(lines) else ""
            for c, key_info in enumerate(row_keys):
                key = key_info[0]
                char = line[c] if c < len(line) else ' '
                color = fg if char != ' ' else bg
                self.set_key_color(key, color)
