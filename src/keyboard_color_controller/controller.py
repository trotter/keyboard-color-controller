class Controller:
    def __init__(self, device):
        self.device = device

    def set_color(self, color):
        self.device.set_color(color)
