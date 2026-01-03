from tkinter import Tk, Frame
from queue import Empty, Queue
from tkmacosx import Button

KEY_WIDTH = 40
KEY_HEIGHT = 40

class Keyboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Keyboard Emulator")
        self.keys = {}
        self.create_keyboard()

    def create_keyboard(self):
        # A simplified 104-key layout with unique names for modifier keys
        layout = [
            [('Esc', 'Esc', 1), ('F1', 'F1', 1), ('F2', 'F2', 1), ('F3', 'F3', 1), ('F4', 'F4', 1), ('F5', 'F5', 1), ('F6', 'F6', 1), ('F7', 'F7', 1), ('F8', 'F8', 1), ('F9', 'F9', 1), ('F10', 'F10', 1), ('F11', 'F11', 1), ('F12', 'F12', 1)],
            [('`', '`', 1), ('1', '1', 1), ('2', '2', 1), ('3', '3', 1), ('4', '4', 1), ('5', '5', 1), ('6', '6', 1), ('7', '7', 1), ('8', '8', 1), ('9', '9', 1), ('0', '0', 1), ('-', '-', 1), ('=', '=', 1), ('Backspace', 'Backspace', 2)],
            [('Tab', 'Tab', 2), ('Q', 'Q', 1), ('W', 'W', 1), ('E', 'E', 1), ('R', 'R', 1), ('T', 'T', 1), ('Y', 'Y', 1), ('U', 'U', 1), ('I', 'I', 1), ('O', 'O', 1), ('P', 'P', 1), ('[', '[', 1), (']', ']', 1), ('\\', '\\', 1)],
            [('CapsLock', 'Caps Lock', 2), ('A', 'A', 1), ('S', 'S', 1), ('D', 'D', 1), ('F', 'F', 1), ('G', 'G', 1), ('H', 'H', 1), ('J', 'J', 1), ('K', 'K', 1), ('L', 'L', 1), (';', ';', 1), ("'", "'", 1), ('Enter', 'Enter', 2)],
            [('LShift', 'Shift', 2.5), ('Z', 'Z', 1), ('X', 'X', 1), ('C', 'C', 1), ('V', 'V', 1), ('B', 'B', 1), ('N', 'N', 1), ('M', 'M', 1), (',', ',', 1), ('.', '.', 1), ('/', '/', 1), ('RShift', 'Shift', 2.5)],
            [('LCtrl', 'Ctrl', 1.5), ('LWin', 'Win', 1.5), ('LAlt', 'Alt', 1.5), ('Space', 'Space', 6), ('RAlt', 'Alt', 1.5), ('Fn', 'Fn', 1.5), ('RCtrl', 'Ctrl', 1.5)]
        ]

        keyboard_frame = Frame(self.master, bd=2, relief='sunken')
        keyboard_frame.pack(padx=10, pady=10)

        for r, row_keys in enumerate(layout):
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
        try:
            message = queue.get_nowait()
            if message['command'] == 'set_all_keys_color':
                keyboard.set_all_keys_color(message['color'])
            elif message['command'] == 'set_key_color':
                keyboard.set_key_color(message['key'], message['color'])
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
