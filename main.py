from tkinter import *
from gui.start_window import StartWindow
from app.configuration import Configuration

Configuration.load()
root = Tk()
app = StartWindow(root)
root.mainloop()
