from tkinter import *
from file_operations import File
from app.configuration import Configuration

class LabelingWindow:

    def __init__(self, master):
        self.root = master
        self.frame = Frame(master)
        self.frame.pack()
        labels = File.read_labels(Configuration.get_selected_game())
        row_count = 0
        for label in labels:
            Label(self.frame, text=label).grid(row=row_count, column=0)
            row_count += 1
        Label(self.frame, text="Enter a new label").grid(row=0, column=1)
        self.label_entry = Entry(self.frame)
        self.label_entry.grid(row=1, column=1)
        Button(self.frame, text="Add label", command=self.add_label).grid(row=2, column=1)
        Label(self.frame).grid(row=3, column=1)
        Button(self.frame, text="Back", command=self.back_to_start_window).grid(row=4, column=1)

    def add_label(self):
        labels = File.read_labels(Configuration.get_selected_game())
        entered_label = self.label_entry.get()
        if not entered_label:
            return
        if not entered_label in labels:
            File.add_label(entered_label)
            Label(self.frame, text=entered_label).grid(row=len(labels), column=0)
            self.root.update()

    def back_to_start_window(self):
        self.root.destroy()
        new_root = Tk()
        from gui.game_options_window import GameOptionsWindow
        app = GameOptionsWindow(new_root)
        new_root.mainloop()
