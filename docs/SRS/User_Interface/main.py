import tkinter as tk
import time
from class_def import *
from tkinter import *
from PIL import Image, ImageTk
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def submitact():
    user = User_input.get()
    passw = Pass_input.get()

    print(f"The name entered by you is {user} {passw}")
    root.destroy()
    win = Tk()
    label = Label(win)
    cap = cv2.VideoCapture(0)
    UserWin = Dis_Window(win, cap, label)

# ---------------------------The following code is used for Tech support window ------------------------------------


def tec_create():
    tech = tk.Tk()
    tech.title("Technical Support")
    tech.geometry("450x300")
    Edward_text = tk.Label(tech, text="Edward He              hey113@mcmaster.ca", font=("Arial", 14))
    Erping_text = tk.Label(tech, text="Erping Zhang          zhange19@mcmaster.ca", font=("Arial", 14))
    Guangwei_text = tk.Label(tech, text="Guangwei Tang      tangg5@mcmaster.ca", font=("Arial", 14))
    Peihua_text = tk.Label(tech, text="Peihua Jin               jinp@mcmaster.ca", font=("Arial", 14))
    Peng_text = tk.Label(tech, text="Peng Cui                cuip1@mcmaster.ca", font=("Arial", 14))

    Edward_text.place(x=40, y=40)
    Erping_text.place(x=40, y=70)
    Guangwei_text.place(x=40, y=100)
    Peihua_text.place(x=40, y=130)
    Peng_text.place(x=40, y=160)

# ----------------------------- Until here for Tech Support Window --------------------------------------------

# ---------------- The following line is about creating the LOGIN Window---------------------------------------


root = tk.Tk()
winreg = root
root.geometry("450x300")
root.title("DBMS Login Page")
User_text = tk.Label(root, text="Username -", )
User_text.place(x=70, y=90)

User_input = tk.Entry(root, width=35)
User_input.place(x=150, y=90, width=200)

Pass_text = tk.Label(root, text="Password -")
Pass_text.place(x=70, y=150)

Pass_input = tk.Entry(root, width=35)
Pass_input.place(x=150, y=150, width=200)

Login = tk.Button(root, text="Login",
                      bg='blue', command=submitact)
Login.place(x=190, y=225, width=70)

Tech_su = tk.Button(root, text = "Tech Support",
                    bg = 'blue', command = tec_create)
Tech_su.place(x=325, y=250, width=100)
# -------------------------------------------- Until Here for LOGIN -------------------------------------------


root.mainloop()
