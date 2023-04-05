from Welcome import *
import tkinter as tk
from diff import *

file_location = "C:/Users/74446/Desktop/test/"
wel_win = tk.Tk()
welcome_window = Welcome_win(wel_win, "Login Page", "450x300", file_location)
welcome_window.content()
