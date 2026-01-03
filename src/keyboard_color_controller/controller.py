from .layout import LAYOUT

class Controller:
    def __init__(self, device):
        self.device = device

    def set_color(self, color):
        self.device.set_color(color)

    def set_key_color(self, key, color):
        self.device.set_key_color(key, color)

    def set_ascii_art(self, art, fg, bg):
        lines = art.splitlines()
        for r, row_keys in enumerate(LAYOUT):
            if r < len(lines):
                line = lines[r]
                for c, key_info in enumerate(row_keys):
                    key = key_info[0]
                    if c < len(line):
                        char = line[c]
                        color = fg if char != ' ' else bg
                        self.set_key_color(key, color)
                    else:
                        self.set_key_color(key, bg)
            else:
                for key_info in row_keys:
                    self.set_key_color(key_info[0], bg)
