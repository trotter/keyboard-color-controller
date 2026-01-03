import tkinter as tk
from queue import Empty, Queue

KEY_WIDTH = 4
KEY_HEIGHT = 2

class Keyboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Keyboard Emulator")
        self.keys = {}
        self.create_keyboard()

    def create_keyboard(self):
        # A simplified 104-key layout
        layout = [
            [('Esc', 1), ('F1', 1), ('F2', 1), ('F3', 1), ('F4', 1), ('F5', 1), ('F6', 1), ('F7', 1), ('F8', 1), ('F9', 1), ('F10', 1), ('F11', 1), ('F12', 1)],
            [('`', 1), ('1', 1), ('2', 1), ('3', 1), ('4', 1), ('5', 1), ('6', 1), ('7', 1), ('8', 1), ('9', 1), ('0', 1), ('-', 1), ('=', 1), ('Backspace', 2)],
            [('Tab', 2), ('Q', 1), ('W', 1), ('E', 1), ('R', 1), ('T', 1), ('Y', 1), ('U', 1), ('I', 1), ('O', 1), ('P', 1), ('[', 1), (']', 1), ('\\', 1)],
            [('Caps Lock', 2), ('A', 1), ('S', 1), ('D', 1), ('F', 1), ('G', 1), ('H', 1), ('J', 1), ('K', 1), ('L', 1), (';', 1), ("'", 1), ('Enter', 2)],
            [('Shift', 2.5), ('Z', 1), ('X', 1), ('C', 1), ('V', 1), ('B', 1), ('N', 1), ('M', 1), (',', 1), ('.', 1), ('/', 1), ('Shift', 2.5)],
            [('Ctrl', 1.5), ('Win', 1.5), ('Alt', 1.5), ('Space', 6), ('Alt', 1.5), ('Fn', 1.5), ('Ctrl', 1.5)]
        ]

        keyboard_frame = tk.Frame(self.master, bd=2, relief=tk.SUNKEN)
        keyboard_frame.pack(padx=10, pady=10)

        for r, row_keys in enumerate(layout):
            col = 0
            for key_text, key_span in row_keys:
                key = tk.Button(keyboard_frame, text=key_text, width=int(KEY_WIDTH * key_span), height=KEY_HEIGHT)
                key.grid(row=r, column=col, columnspan=int(key_span) if key_span > 1 else 1, padx=1, pady=1)
                self.keys[key_text] = key
                col += int(key_span)


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
    run_emulator(q)

if __name__ == "__main__":
    main()
