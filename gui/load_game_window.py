from tkinter import *
from gui.start_window import StartWindow
from gui.game_options_window import GameOptionsWindow
from app.configuration import Configuration
class LoadGameWindow:

  def __init__(self, master):
    self.root = master
    frame = Frame(master)
    frame.pack()
    games = Configuration.get_all_games()
    i = 0
    for game in games:
      btn = Button(frame, text=game)
      btn.config(command=lambda t=game: self.getText(t))
      btn.grid(row=i)
      i += 1
    Label(frame).grid(row=i)
    self.back = Button(frame,
                         text="Back",
                         command=self.back_to_start_window)
    self.back.grid(row=i+1)

  def getText(self, text):
    Configuration.set_selected_game(text)
    self.root.destroy()
    new_root = Tk()
    app = GameOptionsWindow(new_root)
    new_root.mainloop()

  def new_game_profile(self):
    self.root.destroy()
    
  def back_to_start_window(self):
    self.root.destroy()
    new_root = Tk()
    app = StartWindow(new_root)
    new_root.mainloop()

