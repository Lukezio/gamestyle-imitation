from tkinter import *
from gui.start_window import StartWindow
from utils.game_name_utils import GameNameUtils
import file_operations
from file_operations import Directory
from app.configuration import Configuration
from gui.game_options_window import GameOptionsWindow

class NewGameWindow:

  def __init__(self, master):
    self.root = master
    frame = Frame(master)
    frame.pack()
    self.create_profile_label = Label(frame, text="Name of the game")
    self.create_profile_label.grid(row=0)
    self.game_name = Entry(frame)
    self.game_name.grid(row=1)
    self.new_game = Button(frame,
                         text="Create Game Profile",
                         command=self.create_new_game_profile)
    self.new_game.grid(row=2)
    self.error_msg_label = Label(frame, text="")
    self.error_msg_label.grid(row=3)
    self.back = Button(frame,
                         text="Back",
                         command=self.back_to_start_window)
    self.back.grid(row=4)

  def create_new_game_profile(self):
    if not self.game_name.get():
      self.error_msg_label.config(text='The input string is empty')
      self.error_msg_label.config(fg='red')
      return
    name = GameNameUtils.normalized_name(self.game_name.get())
    if Configuration.game_profile_exists(name):
      self.error_msg_label.config(text='This game already has a profile')
      self.error_msg_label.config(fg='red')
      self.root.update()
    else:
      self.error_msg_label.config(text='')
      self.root.update()
      Configuration.add_game_profile(name)
      Configuration.set_selected_game(name)
      Directory.create_game_directories(name)
      self.root.destroy()
      new_root = Tk()
      app = GameOptionsWindow(new_root)
      new_root.mainloop()
    
  def back_to_start_window(self):
    self.root.destroy()
    new_root = Tk()
    app = StartWindow(new_root)
    new_root.mainloop()

