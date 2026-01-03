# This file will contain the keyboard emulator GUI
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Keyboard Emulator")
    label = tk.Label(root, text="Keyboard Emulator")
    label.pack(padx=20, pady=20)
    root.mainloop()

if __name__ == "__main__":
    main()
