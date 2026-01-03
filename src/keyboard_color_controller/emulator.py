from tkinter import Tk, Frame
from queue import Empty, Queue
from tkmacosx import Button

from .layout import LAYOUT

KEY_WIDTH = 40
KEY_HEIGHT = 40

class Keyboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Keyboard Emulator")
        self.keys = {}
        self.create_keyboard()

    def create_keyboard(self):
        keyboard_frame = Frame(self.master, bd=2, relief='sunken')
        keyboard_frame.pack(padx=10, pady=10)

        for r, row_keys in enumerate(LAYOUT):
            col = 0
            for unique_name, display_text, key_span in row_keys:
                key = Button(keyboard_frame, text=display_text, width=int(KEY_WIDTH * key_span), height=KEY_HEIGHT)
                key.grid(row=r, column=col, columnspan=int(key_span) if key_span > 1 else 1, padx=1, pady=1)
                self.keys[unique_name] = key
                col += int(key_span)


    def set_key_color(self, key_name, color):
        if key_name in self.keys:
            self.keys[key_name].config(bg=color)

    def set_all_keys_color(self, color):
        for key in self.keys.values():
            key.config(bg=color)

def run_emulator(queue):
    root = Tk()
    keyboard = Keyboard(root)

    def check_queue():
        while True:
            try:
                message = queue.get_nowait()
                if message['command'] == 'set_all_keys_color':
                    keyboard.set_all_keys_color(message['color'])
                elif message['command'] == 'set_key_color':
                    keyboard.set_key_color(message['key'], message['color'])
            except Empty:
                break
        root.after(10, check_queue)

    root.after(100, check_queue)
    root.mainloop()

def main():
    # This main function is for standalone testing of the emulator
    q = Queue()
    run_emulator(q)

if __name__ == "__main__":
    main()
