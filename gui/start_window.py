from tkinter import *
class StartWindow:

  def __init__(self, master):
    self.root = master
    frame = Frame(master)
    frame.pack()
    self.new_game = Button(frame,
                         text="New Game Profile",
                         command = self.new_game_profile)
    self.new_game.pack(side=TOP)
    self.load_game = Button(frame,
                         text="Load Game Profile",
                         command = self.load_game_profile)
    self.load_game.pack(side=BOTTOM)

  def new_game_profile(self):
    self.root.destroy()
    new_root = Tk()
    from gui.new_game_window import NewGameWindow
    app = NewGameWindow(new_root)
    new_root.mainloop()
    
  def load_game_profile(self):
    self.root.destroy()
    new_root = Tk()
    from gui.load_game_window import LoadGameWindow
    app = LoadGameWindow(new_root)
    new_root.mainloop()

