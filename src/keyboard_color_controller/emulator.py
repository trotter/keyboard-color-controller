import tkinter as tk
from queue import Empty, Queue

KEY_WIDTH = 6
KEY_HEIGHT = 3

class Keyboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Keyboard Emulator")
        self.keys = {}
        self.create_keyboard()

    def create_keyboard(self):
        layout = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
            ['Caps Lock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'Enter'],
            ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Alt', 'Space', 'Alt', 'Ctrl']
        ]

        for r, row_keys in enumerate(layout):
            row_frame = tk.Frame(self.master)
            row_frame.pack()
            for c, key_text in enumerate(row_keys):
                key = tk.Button(row_frame, text=key_text, width=KEY_WIDTH, height=KEY_HEIGHT)
                if key_text == 'Space':
                    key.config(width=30)
                key.pack(side=tk.LEFT, padx=2, pady=2)
                self.keys[key_text] = key

    def set_key_color(self, key_text, color):
        if key_text in self.keys:
            self.keys[key_text].config(bg=color)

    def set_all_keys_color(self, color):
        for key in self.keys.values():
            key.config(bg=color)

def run_emulator(queue):
    root = tk.Tk()
    keyboard = Keyboard(root)

    def check_queue():
        try:
            message = queue.get_nowait()
            if message['command'] == 'set_all_keys_color':
                keyboard.set_all_keys_color(message['color'])
        except Empty:
            pass
        root.after(100, check_queue)

    root.after(100, check_queue)
    root.mainloop()

def main():
    # This main function is for standalone testing of the emulator
    q = Queue()
    # To test, you can put messages in the queue, e.g.:
    # q.put({'command': 'set_all_keys_color', 'color': 'blue'})
    run_emulator(q)

if __name__ == "__main__":
    main()
