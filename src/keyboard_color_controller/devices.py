from abc import ABC, abstractmethod
import multiprocessing
from .emulator import run_emulator

class Device(ABC):
    @abstractmethod
    def set_color(self, color):
        pass

    @abstractmethod
    def set_key_color(self, key, color):
        pass

class OpenRGBDevice(Device):
    def __init__(self):
        # TODO: Initialize OpenRGB client here
        print("Connecting to real keyboard...")
        pass

    def set_color(self, color):
        # TODO: OpenRGB logic to set color
        print(f"Setting color to {color} on real keyboard")

    def set_key_color(self, key, color):
        # TODO: OpenRGB logic to set key color
        print(f"Setting key {key} to {color} on real keyboard")

class EmulatorDevice(Device):
    def __init__(self):
        self.queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=run_emulator, args=(self.queue,))
        self.process.start()

    def set_color(self, color):
        self.queue.put({'command': 'set_all_keys_color', 'color': color})

    def set_key_color(self, key, color):
        self.queue.put({'command': 'set_key_color', 'key': key, 'color': color})

    def __del__(self):
        self.process.terminate()
