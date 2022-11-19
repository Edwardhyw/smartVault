# Import required Libraries
import time
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# ----------------------------- The class definition of Display Window -----------------------------------


class Dis_Window:
   def __init__(self, window, cap, label):
      # Create an instance of Tkinter Window or frame
      self.window = window
      self.window.title("Main Window")
      # Set the size of the window
      self.window.geometry("1500x800")
      self.cap = cap
      self.label = label
      self.label.grid(row=0, column=0)
      self.hand_detect()

   def hand_detect(self):
      with mp_hands.Hands(
              model_complexity=0,
              min_detection_confidence=0.5,
              min_tracking_confidence=0.5) as hands:
         # Get the latest frame and convert into Image
         image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)

         # To improve performance, optionally mark the image as not writeable to
         # pass by reference.
         results = hands.process(image)

         # Draw the hand annotations on the image.
         image.flags.writeable = True
         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
         if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
               mp_drawing.draw_landmarks(
                  image,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  mp_drawing_styles.get_default_hand_landmarks_style(),
                  mp_drawing_styles.get_default_hand_connections_style())

      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      image = cv2.flip(image, 1)
      img = Image.fromarray(image)
      img = img.resize((1000, 800), Image.ANTIALIAS)
      # Convert image to PhotoImage
      imgtk = ImageTk.PhotoImage(image=img)
      self.label.imgtk = imgtk
      self.label.configure(image=imgtk)
      # Repeat after an interval to capture continuously
      self.label.after(20, self.hand_detect)

# ------------------------------------------- End of Definition -------------------------------------------