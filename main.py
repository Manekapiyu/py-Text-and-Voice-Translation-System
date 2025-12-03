from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter.ttk import Combobox
import os
import tempfile
import PyPDF2
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound3  

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

# Display list 
language_display_list = [name.title() for name in supported_languages.keys()]

def get_lang_code(display_name: str) -> str:
    # Map Title Case display back to code using lowercase keys
    return supported_languages.get(display_name.strip().lower(), "en")


root = Tk()
root.title("Text Translate Tool")
root.geometry("1100x650+190+50")
root.config(bg=bodybg)

# Safe image loader 
def load_image(path: str):
    try:
        return PhotoImage(file=path)
    except Exception:
        return None

def create_image_button(img, x, y, command=None, fallback_text="Button"):
    if img:
        btn = Button(root, image=img, bd=0, bg=bodybg, activebackground=bodybg, relief=FLAT, command=command)
    else:
        btn = Button(root, text=fallback_text, bd=0, bg=bodybg, activebackground=bodybg, relief=FLAT, command=command)
    btn.place(x=x, y=y)
    return btn

icon_img = load_image("Images/icon.png")
if icon_img:
    root.iconphoto(False, icon_img)

Top_frame = Frame(root, bg=framebg, width=1100, height=130)
Top_frame.place(x=0, y=0)

logo_icon = load_image("Images/icon.png")
if logo_icon:
    Label(Top_frame, image=logo_icon, bg=framebg).place(x=40, y=20)
Label(Top_frame, text="TEXT TRANSLATE TOOL", font="Arial 20 bold",
      bg=framebg, fg="#ffffff").place(x=180, y=48)

# Text areas
text_area1 = Text(root, font="Arial 16", bg=text1_bg, relief=GROOVE, wrap=WORD)
text_area1.place(x=30, y=180, width=600, height=180)

text_area2 = Text(root, font="Arial 16", bg=text2_bg, relief=GROOVE, wrap=WORD)
text_area2.place(x=30, y=400, width=600, height=180)

# Language selection
combo1 = ttk.Combobox(root, values=language_display_list, font="Arial 14", state="readonly", width=12)
combo1.place(x=60, y=140)
combo1.set("English")

combo2 = ttk.Combobox(root, values=language_display_list, font="Arial 14", state="readonly", width=12)
combo2.place(x=250, y=140)
combo2.set("Sinhala")

# Voice and speed labels
Label(root, text="VOICE", font="Arial 14", bg=bodybg, fg=label_fg).place(x=700, y=300)
Label(root, text="SPEED", font="Arial 14", bg=bodybg, fg=label_fg).place(x=700, y=350)

# Gender combo
gender_combobox = Combobox(root, values=["Male", "Female"], font="Arial 14", state="readonly", width=10)
gender_combobox.place(x=800, y=300)
gender_combobox.set("Male")

# Speed slider 
current_value = DoubleVar(value=120.0)

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

def convert_text():
    source_text = text_area1.get("1.0", END).strip()
    if not source_text:
        messagebox.showwarning("Warning", "Please enter text to translate")
        return

    target_lang = get_lang_code(combo2.get())
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(source_text)
        text_area2.delete("1.0", END)
        text_area2.insert(END, translated)
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed:\n{str(e)}")

def speak_text():
    text = text_area2.get("1.0", END).strip()
    if not text:
        messagebox.showwarning("Warning", "No text to speak")
        return

    lang_code = get_lang_code(combo2.get())

    # Use a temporary file for audio
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_audio = os.path.join(tmpdir, "temp.mp3")
            tts = gTTS(text=text, lang=lang_code)
            tts.save(temp_audio)
            playsound3.playsound(temp_audio)
    except Exception as e:
        messagebox.showerror("Error", f"Text-to-speech failed:\n{str(e)}")

def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return

    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            extracted_text = []
            for page in reader.pages:
                page_text = page.extract_text() or ""
                extracted_text.append(page_text)
            text = "\n".join(extracted_text).strip()

        if not text:
            messagebox.showinfo("Info", "No extractable text found in this PDF.")
            return

        text_area1.delete("1.0", END)
        text_area1.insert(END, text)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF:\n{str(e)}")

def upload_audio():
    messagebox.showinfo("Info", "Audio upload feature not implemented yet")

def save_translated_text():
    text = text_area2.get("1.0", END).strip()
    if not text:
        messagebox.showwarning("Warning", "No translated text to save")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("Success", "Translated text saved successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

# buttons
speak_icon = load_image("Images/speak.png")
create_image_button(speak_icon, 700, 450, command=speak_text, fallback_text="Speak")

download_icon = load_image("Images/download.png")
create_image_button(download_icon, 860, 450, command=save_translated_text, fallback_text="Save")

pdf_icon = load_image("Images/pdfimage.png")
create_image_button(pdf_icon, 680, 48, command=upload_pdf, fallback_text="Upload PDF")

music_icon = load_image("Images/music.png")
create_image_button(music_icon, 750, 48, command=upload_audio, fallback_text="Upload Audio")

trans_icon = load_image("Images/trans.png")
create_image_button(trans_icon, 810, 48, command=convert_text, fallback_text="Translate")

other_speaker_icon = load_image("Images/otherspeaker.png")
create_image_button(other_speaker_icon, 50, 525, command=speak_text, fallback_text="Speak")

mic_icon = load_image("Images/mic.png")
create_image_button(mic_icon, 50, 305, command=upload_audio, fallback_text="Mic")

# PDF/Text mode button
button_mode = True
choice = "Text"
textmode_img = load_image("Images/modeText.png")
pdfmode_img = load_image("Images/modepdf.png")

def change_mode():
    global button_mode, choice
    if button_mode:
        choice = "PDF"
        mode.config(image=pdfmode_img if pdfmode_img else "")
        if not pdfmode_img:
            mode.config(text="PDF Mode")
        button_mode = False
    else:
        choice = "Text"
        mode.config(image=textmode_img if textmode_img else "")
        if not textmode_img:
            mode.config(text="Text Mode")
        button_mode = True

mode = Button(
    root,
    image=textmode_img if textmode_img else None,
    text="" if textmode_img else "Text Mode",
    bd=0, bg=framebg, relief=FLAT,
    command=change_mode, fg="#ffffff", activebackground=framebg
)
mode.place(x=900, y=30)

# Translate button
convert_btn = Button(root, text="Translate", font=("Arial", 14, "bold"), command=convert_text)
convert_btn.place(x=400, y=140, width=100, height=30)

root.mainloop()
