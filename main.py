from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter.ttk import Combobox
import os
import PyPDF2
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound3     # using your original playsound3 API as requested

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

# Icon
image_icon = PhotoImage(file="Images/icon.png")
root.iconphoto(False, image_icon)

# Top frame
Top_frame = Frame(root, bg=framebg, width=1100, height=130)
Top_frame.place(x=0, y=0)
logo_icon = PhotoImage(file="Images/icon.png")
Label(Top_frame, image=logo_icon, bg=framebg).place(x=40, y=20)
Label(Top_frame, text="TEXT TRANSLATE TOOL", font="Arial 20 bold",
      bg=framebg, fg="#ffffff").place(x=180, y=48)

# Text areas
text_area1 = Text(root, font="Arial 16", bg=text1_bg, relief=GROOVE, wrap=WORD)
text_area1.place(x=30, y=180, width=600, height=180)
text_area2 = Text(root, font="Arial 16", bg=text2_bg, relief=GROOVE, wrap=WORD)
text_area2.place(x=30, y=400, width=600, height=180)

# Language selection
combo1 = ttk.Combobox(root, values=language_list, font="Arial 14", state="readonly", width=12)
combo1.place(x=60, y=140)
combo1.set("ENGLISH")
combo2 = ttk.Combobox(root, values=language_list, font="Arial 14", state="readonly", width=12)
combo2.place(x=250, y=140)
combo2.set("SINHALA")

# Voice and speed labels
Label(root, text="VOICE", font="Arial 14", bg=bodybg, fg=label_fg).place(x=700, y=300)
Label(root, text="SPEED", font="Arial 14", bg=bodybg, fg=label_fg).place(x=700, y=350)

# Gender combo
gender_combobox = Combobox(root, values=["Male", "Female"], font="Arial 14", state="readonly", width=10)
gender_combobox.place(x=800, y=300)
gender_combobox.set("Male")

# Speed slider
current_value = DoubleVar()
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

# Function: Translate text
def convert_text():
    text = text_area1.get("1.0", END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter text to translate")
        return
    target_lang = supported_languages.get(combo2.get().lower(), "en")
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        text_area2.delete("1.0", END)
        text_area2.insert(END, translated)
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed:\n{str(e)}")

# Function: Speak text
def speak_text():
    text = text_area2.get("1.0", END).strip()
    if not text:
        messagebox.showwarning("Warning", "No text to speak")
        return
    tts = gTTS(text=text, lang=supported_languages.get(combo2.get().lower(), "en"))
    tts.save("temp.mp3")
    playsound3.playsound("temp.mp3")  
    os.remove("temp.mp3")


# Function: Upload PDF
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            text_area1.delete("1.0", END)
            text_area1.insert(END, text)

# Placeholder for audio upload
def upload_audio():
    messagebox.showinfo("Info", "Audio upload feature not implemented yet")

# Buttons with no background
def create_image_button(img, x, y, command=None):
    btn = Button(root, image=img, bd=0, bg=bodybg, activebackground=bodybg, relief=FLAT, command=command)
    btn.place(x=x, y=y)
    return btn

image_icon = PhotoImage(file="Images/speak.png")
btn = create_image_button(image_icon, 700, 450)

image_icon2 = PhotoImage(file="Images/download.png")
save = create_image_button(image_icon2, 860, 450)

pdfupload = PhotoImage(file="Images/pdfimage.png")
upload_button = create_image_button(pdfupload, 680, 48, upload_pdf)

upload_audioimage = PhotoImage(file="Images/music.png")
upload_audio_button = create_image_button(upload_audioimage, 750, 48, upload_audio)

transimage = PhotoImage(file="Images/trans.png")
trans_image_button = create_image_button(transimage, 810, 48, convert_text)

speakimage = PhotoImage(file="Images/otherspeaker.png")
speak_button = create_image_button(speakimage, 50, 525, speak_text)

micimage = PhotoImage(file="Images/mic.png")
mic_button = create_image_button(micimage, 50, 305)

# PDF/Text mode toggle
button_mode = True
choice = "Text"
textmode = PhotoImage(file="Images/modeText.png")
pdfmode = PhotoImage(file="Images/modepdf.png")
def chnagemode():
    global button_mode, choice
    if button_mode:
        choice = "PDF"
        mode.config(image=pdfmode)
        button_mode = False
    else:
        choice = "Text"
        mode.config(image=textmode)
        button_mode = True
mode = Button(root, image=textmode, bd=0, bg=framebg, relief=FLAT, command=chnagemode)
mode.place(x=900, y=30)

# Translate button
convert_btn = Button(root, text="Translate", font=("Arial", 14, "bold"), command=convert_text)
convert_btn.place(x=450, y=140, width=100, height=30)

root.mainloop()
