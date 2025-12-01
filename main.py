from tkinter import *
from tkinter import messagebox,filedialog
from tkinter import ttk
from tkinter.ttk import Combobox
import tkinter as tk

import speech_recognition as sr
import PyPDF2
import pyttsx3
import os

import googletrans
from googletrans import Translator

import datetime
from gtts import gTTS
from playsound3 import playsound3
import threading

framebg="#161d3f"
bodybg="#84a1e8"

root=Tk()
root.title("Text to Speech and Speech to Text Application")
root.geometry("1030x57+290+140")
root.config(bg="lightblue")

#icons
image_icon=PhotoImage(file="Images/icon.png")
root.iconphoto(False,image_icon)

#Top Frame
Top_frame = Frame(root,bg=framebg,width=1100, height=130)
Top_frame.place(x=0, y=0)

logo_icon

root.mainloop()


