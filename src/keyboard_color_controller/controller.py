class Controller:
    def __init__(self, device):
        self.device = device

    def set_color(self, color):
        self.device.set_color(color)

    def set_key_color(self, key, color):
        self.device.set_key_color(key, color)
