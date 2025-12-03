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
text2_bg = "#e8efff"   
label_fg = "#000000"   


supported_languages = {
    "english": "en", "hindi": "hi", "spanish": "es", "french": "fr", "german": "de",
    "chinese": "zh", "japanese": "ja", "korean": "ko", "arabic": "ar", "russian": "ru",
    "italian": "it", "portuguese": "pt", "turkish": "tr", "sinhala": "si"  
}

language_list = list(supported_languages.keys())


root = Tk()
root.title("Text Translate Tool")
root.geometry("1100x650+190+50")
root.config(bg=bodybg)


image_icon = PhotoImage(file="Images/icon.png")
root.iconphoto(False, image_icon)


Top_frame = Frame(root, bg=framebg, width=1100, height=130)
Top_frame.place(x=0, y=0)

logo_icon = PhotoImage(file="Images/icon.png")
Label(Top_frame, image=logo_icon, bg=framebg).place(x=40, y=20)

Label(
    Top_frame,
    text="TEXT TRANSLATE TOOL",
    font="Arial 20 bold",
    bg=framebg,
    fg="#ffffff"
).place(x=180, y=48)


text_area1 = Text(root, font="Arial 16", bg=text1_bg, relief=GROOVE, wrap=WORD)
text_area1.place(x=30, y=180, width=600, height=180)

text_area2 = Text(root, font="Arial 16", bg=text2_bg, relief=GROOVE, wrap=WORD)
text_area2.place(x=30, y=400, width=600, height=180)


combo1 = ttk.Combobox(root, values=language_list, font="Arial 14", state="readonly", width=12)
combo1.place(x=60, y=140)
combo1.set("ENGLISH")

combo2 = ttk.Combobox(root, values=language_list, font="Arial 14", state="readonly", width=12)
combo2.place(x=250, y=140)
combo2.set("SINHALA")

Label(root, text="VOICE", font="Arial 14", bg=bodybg, fg=label_fg).place(x=700, y=300)
Label(root, text="SPEED", font="Arial 14", bg=bodybg, fg=label_fg).place(x=700, y=350)

gender_combobox = Combobox(root, values=["Male", "Female"], font="Arial 14", state="readonly", width=10)
gender_combobox.place(x=800, y=300)
gender_combobox.set("Male")

current_value = tk.DoubleVar()

def get_current_value():
    return "{: .2f}".format(current_value.get())

def slider_changed(event):
    value_label.config(text=get_current_value())

style = ttk.Style()
style.configure("TScale", background=bodybg)

slider = ttk.Scale(root, from_=30, to=250, orient=HORIZONTAL, length=150,
                   variable=current_value, command=slider_changed)
slider.place(x=800, y=350)

value_label = Label(root, text=get_current_value(), font=("Arial", 12), bg=bodybg)
value_label.place(x=960, y=350)

#Buttons
image_icon=PhotoImage(file="Images/speak.png")
btn=Button(root,compound=LEFT,image=image_icon)
btn.place(x=700, y=450)

image_icon2=PhotoImage(file="Images/download.png")
save=Button(root,compound=LEFT,image=image_icon2)
save.place(x=830, y=450)

pdfupload=PhotoImage(file="Images/pdfimage.png")
upload_button=Button(root,compound=LEFT,image=pdfupload)
upload_button.place(x=680, y=48)

upload_audioimage=PhotoImage(file="Images/music.png")
upload_audio_button=Button(root,compound=LEFT,image=upload_audioimage)
upload_audio_button.place(x=750,y=48)

transimage=PhotoImage(file="Images/trans.png")
trans_image_button=Button(root,compound=LEFT,image=transimage)
trans_image_button.place(x=810,y=48)

speakimage=PhotoImage(file="Images/otherspeaker.png")
speak_button=Button(root,compound=LEFT,image=speakimage)
speak_button.place(x=50,y=525)

micimage=PhotoImage(file="Images/mic.png")
mic_button=Button(root,compound=LEFT,image=micimage)
mic_button.place(x=50,y=305)


#pdf and text mode button
button_mode=True
choice="Text"

def chnagemode():
    global button_mode
    global choice
    if button_mode:
        choice="PDF"
        mode.config(image=pdfmode,activebackground=framebg)
        button_mode=False

    else:
        choice="Text"
        mode.config(image=textmode,activebackground=framebg)
        button_mode=True




textmode=PhotoImage(file="Images/modeText.png")
pdfmode=PhotoImage(file="Images/modepdf.png")
mode=Button(root,image=textmode,bg=framebg,bd=0,command=chnagemode)
mode.place(x=900,y=30)




def convert_text():
    text = text_area1.get("1.0", END)
    target_lang = supported_languages[combo2.get().lower()]
    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
    text_area2.delete("1.0", END)
    text_area2.insert(END, translated)

convert_btn = Button(root, text="Translate", font=("Arial", 14, "bold"), command=convert_text)
convert_btn.place(x=450, y=140, width=100, height=30)



root.mainloop()
