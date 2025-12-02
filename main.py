from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkinter.ttk import Combobox
import tkinter as tk

import speech_recognition as sr
import PyPDF2
import pyttsx3
import os

from deep_translator import GoogleTranslator

import datetime
from gtts import gTTS
from playsound3 import playsound3
import threading


framebg = "#14213d"
bodybg = "#e5e5e5"
text1_bg = "#dff6ff"
text2_bg = "#e8e8ff"


supported_languages = {
    "english": "en", "hindi": "hi", "spanish": "es", "french": "fr", "german": "de",
    "chinese": "zh", "japanese": "ja", "korean": "ko", "arabic": "ar", "russian": "ru",
    "italian": "it", "portuguese": "pt", "turkish": "tr", "sinhala": "si"     # ← Added Sinhala
}

language_list = list(supported_languages.keys())

root = Tk()
root.title("Text to Speech and Speech to Text Application")
root.geometry("1100x650+190+50")
root.config(bg=bodybg)

# Icon
image_icon = PhotoImage(file="Images/icon.png")
root.iconphoto(False, image_icon)

# Top Frame
Top_frame = Frame(root, bg=framebg, width=1100, height=130)
Top_frame.place(x=0, y=0)

logo_icon = PhotoImage(file="Images/icon.png")
Label(Top_frame, image=logo_icon, bg=framebg).place(x=40, y=20)

Label(
    Top_frame,
    text="TEXT TOOL",
    font="Arial 28 bold",
    bg=framebg,
    fg="#ffffff"
).place(x=200, y=35)


text_area1 = Text(root, font="Arial 16", bg=text1_bg, relief=GROOVE, wrap=WORD)
text_area1.place(x=40, y=160, width=600, height=180)


text_area2 = Text(root, font="Arial 16", bg=text2_bg, relief=GROOVE, wrap=WORD)
text_area2.place(x=40, y=380, width=600, height=180)


combo1 = ttk.Combobox(root, values=language_list, font="arial 14", state="readonly", width=12)
combo1.place(x=700, y=200)
combo1.set("ENGLISH")

combo2 = ttk.Combobox(root, values=language_list, font="arial 14", state="readonly", width=12)
combo2.place(x=700, y=260)
combo2.set("SINHALA") 

#voice and speed labels and controls
Label(root, text="Voice:", font="Arial 14", bg=bodybg , fg="#000000").place(x=700, y=320)
root.mainloop()
