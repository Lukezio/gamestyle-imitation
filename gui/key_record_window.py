from tkinter import *
from file_operations import File
from app.configuration import Configuration
from pynput.keyboard import Key, Listener, Controller
from threading import Thread

last_selected_key = StringVar()

def detect_keys():
    with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

def on_press(key):
    return

def on_release(key):
    global last_selected_key
    last_selected_key.set(str(key))
    if key == Key.esc:
        # Stop listener
        return False

class KeyRecordWindow:
    def __init__(self, master):
        global last_selected_key
        last_selected_key = StringVar()
        self.root = master
        self.frame = Frame(master)
        self.frame.pack()
        keys = File.read_keys(Configuration.get_selected_game())
        row_count = 0
        for key in keys:
            Label(self.frame, text=key).grid(row=row_count, column=0)
            row_count += 1
        Label(self.frame, text="Enter a key command").grid(row=0, column=1)
        self.selected_key = Label(self.frame, textvariable=last_selected_key)
        self.selected_key.grid(row=1, column=1)
        Button(self.frame, text="Add key", command=self.add_key).grid(row=2, column=1)
        Label(self.frame).grid(row=3, column=1)
        Button(self.frame, text="Back", command=self.back_to_start_window).grid(row=4, column=1)
        self.thread = Thread(target=detect_keys)
        self.thread.start()

    def add_key(self):
        keys = File.read_keys(Configuration.get_selected_game())
        global last_selected_key
        selected_key = last_selected_key.get()
        if not selected_key:
            print('no key entered yet')
            return
        if not selected_key in keys:
            File.add_key(selected_key)
            Label(self.frame, text=selected_key).grid(row=len(keys), column=0)
            self.root.update()
        return

    def back_to_start_window(self):
        keyboard = Controller()
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        self.root.destroy()
        new_root = Tk()
        from gui.game_options_window import GameOptionsWindow
        app = GameOptionsWindow(new_root)
        new_root.mainloop()
