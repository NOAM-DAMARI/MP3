import os
import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
from pydub import AudioSegment

# סיומות קובצי שמע נתמכים
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".aac"}

# פונקציה ליצירת הקדמה קולית ושמירת קובץ חדש

def process_audio_files(files):
    output_dir = "processed_audio"
    os.makedirs(output_dir, exist_ok=True)
    
    for file in files:
        file_path = os.path.abspath(file)
        file_name, ext = os.path.splitext(os.path.basename(file))
        if ext.lower() not in AUDIO_EXTENSIONS:
            continue
        
        # יצירת קובץ שמע מהשם של הקובץ
        tts = gTTS(text=file_name, lang="he")
        intro_path = os.path.join(output_dir, f"intro_{file_name}.mp3")
        tts.save(intro_path)
        
        # שילוב ההקדמה עם הקובץ המקורי
        intro = AudioSegment.from_file(intro_path, format="mp3")
        audio = AudioSegment.from_file(file_path, format=ext[1:])
        combined = intro + audio
        
        output_path = os.path.join(output_dir, f"processed_{file_name}.mp3")
        combined.export(output_path, format="mp3")
        print(f"Processed: {output_path}")
    
    messagebox.showinfo("השלמה", "כל הקבצים עובדו ונשמרו בתיקייה processed_audio")

# פונקציות לפתיחת קבצים ותיקיות

def open_files():
    files = filedialog.askopenfilenames(title="בחר קבצי שמע", filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg;*.flac;*.aac")])
    process_audio_files(files)

def open_folder():
    folder = filedialog.askdirectory(title="בחר תיקייה עם קבצים")
    if folder:
        files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS]
        process_audio_files(files)

# ממשק גרפי עם Tkinter
root = tk.Tk()
root.title("מעבד קבצי שמע עם שם הקובץ בעברית")
root.geometry("400x200")

btn_files = tk.Button(root, text="בחר קבצים", command=open_files, width=20)
btn_files.pack(pady=10)

btn_folder = tk.Button(root, text="בחר תיקייה", command=open_folder, width=20)
btn_folder.pack(pady=10)

root.mainloop()
