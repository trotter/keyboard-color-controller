from abc import ABC, abstractmethod
import multiprocessing
from .emulator import run_emulator
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType

COLOR_MAP = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
}

def get_rgb(color_name):
    rgb = COLOR_MAP.get(color_name.lower(), (255, 255, 255))
    return RGBColor(*rgb)

class Device(ABC):
    @abstractmethod
    def set_color(self, color):
        pass

    @abstractmethod
    def set_key_color(self, key, color):
        pass

class OpenRGBDevice(Device):
    def __init__(self):
        print("Connecting to OpenRGB server...")
        self.client = OpenRGBClient()
        self.device = None
        
        # Find the first keyboard
        for device in self.client.devices:
            if device.type == DeviceType.KEYBOARD:
                self.device = device
                break
        
        if not self.device:
            print("No keyboard found via OpenRGB. Using the first available device.")
            if self.client.devices:
                self.device = self.client.devices[0]
            else:
                raise Exception("No OpenRGB devices found. Make sure OpenRGB is running.")

        print(f"Connected to {self.device.name}")

    def set_color(self, color):
        rgb = get_rgb(color)
        self.device.set_color(rgb)

    def set_key_color(self, key, color):
        rgb = get_rgb(color)
        # Try to find the LED by name. OpenRGB names are often "Key: <name>"
        led = None
        # Exact match
        led = next((l for l in self.device.leds if l.name.lower() == key.lower()), None)
        if not led:
            # Match with "Key: " prefix
            led = next((l for l in self.device.leds if l.name.lower() == f"key: {key.lower()}"), None)
        if not led:
            # Partial match
            led = next((l for l in self.device.leds if key.lower() in l.name.lower()), None)

        if led:
            led.set_color(rgb)
        else:
            # Fallback or just ignore
            pass

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
        if hasattr(self, 'process'):
            self.process.terminate()