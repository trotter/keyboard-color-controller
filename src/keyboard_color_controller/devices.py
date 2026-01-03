from abc import ABC, abstractmethod
import multiprocessing
from typing import Tuple, Optional
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

def hex_to_rgb(hex_color: str) -> Optional[Tuple[int, int, int]]:
    """Converts a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    try:
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 3:
            return tuple(int(hex_color[i]*2, 16) for i in (0, 1, 2))
    except ValueError:
        return None
    return None

def get_rgb(color_name: str) -> RGBColor:
    """Gets an RGBColor object from a name or hex string."""
    if color_name.startswith('#'):
        rgb = hex_to_rgb(color_name)
        if rgb:
            return RGBColor(*rgb)
    
    # Try named color
    rgb = COLOR_MAP.get(color_name.lower())
    if rgb:
        return RGBColor(*rgb)
        
    # Fallback to white if unknown
    return RGBColor(255, 255, 255)

class Device(ABC):
    @abstractmethod
    def set_color(self, color: str) -> None:
        pass

    @abstractmethod
    def set_key_color(self, key: str, color: str) -> None:
        pass

class OpenRGBDevice(Device):
    def __init__(self) -> None:
        print("Connecting to OpenRGB server...")
        try:
            self.client = OpenRGBClient()
        except Exception as e:
            raise RuntimeError(f"Could not connect to OpenRGB server: {e}. Is it running?")
            
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
                raise RuntimeError("No OpenRGB devices found.")

        print(f"Connected to {self.device.name}")

    def set_color(self, color: str) -> None:
        rgb = get_rgb(color)
        self.device.set_color(rgb)

    def set_key_color(self, key: str, color: str) -> None:
        rgb = get_rgb(color)
        # Try to find the LED by name. OpenRGB names are often "Key: <name>"
        led = None
        key_lower = key.lower()
        
        # Exact match
        led = next((l for l in self.device.leds if l.name.lower() == key_lower), None)
        if not led:
            # Match with "Key: " prefix
            led = next((l for l in self.device.leds if l.name.lower() == f"key: {key_lower}"), None)
        if not led:
            # Partial match
            led = next((l for l in self.device.leds if key_lower in l.name.lower()), None)

        if led:
            led.set_color(rgb)

class EmulatorDevice(Device):
    def __init__(self) -> None:
        self.queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=run_emulator, args=(self.queue,))
        self.process.start()

    def set_color(self, color: str) -> None:
        self.queue.put({'command': 'set_all_keys_color', 'color': color})

    def set_key_color(self, key: str, color: str) -> None:
        self.queue.put({'command': 'set_key_color', 'key': key, 'color': color})

    def __del__(self) -> None:
        if hasattr(self, 'process') and self.process.is_alive():
            self.process.terminate()
            self.process.join()