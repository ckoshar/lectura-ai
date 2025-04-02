import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys
from transcribe import transcribe as run_transcription
from summary import append_summary_to_file


# Cross-platform folder for saving transcripts
def get_notes_folder():
    home = os.path.expanduser("~")
    notes_folder = os.path.join(home, "Lectura", "notes")
    os.makedirs(notes_folder, exist_ok=True)
    return notes_folder

# Dummy transcribe function (replace with real logic later)
def transcribe_audio(file_path):
    filename = os.path.splitext(os.path.basename(file_path))[0]
    notes_folder = get_notes_folder()
    transcript_path = os.path.join(notes_folder, f"{filename}.txt")

    with open(transcript_path, "w") as f:
        f.write(f"Transcript for {filename}\n\n[Simulated content here]\n")

    return transcript_path

# Handles selecting a file and running transcription

def select_audio():
    file_path = filedialog.askopenfilename(
        title="Select an Audio File",
        filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.aac *.ogg")]
    )
    if file_path:
        try:
            transcript_path = run_transcription(file_path)
            append_summary_to_file(transcript_path)

            messagebox.showinfo("Done", f"Transcript and summary saved to:\n{transcript_path}")
            open_file(transcript_path)

        except Exception as e:
            messagebox.showerror("Error", f"Failed during processing:\n{str(e)}")


# Cross-platform file opener
def open_file(file_path):
    try:
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.call(['open', file_path])
        elif os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # Linux
            subprocess.call(['xdg-open', file_path])
        else:
            messagebox.showinfo("Note", f"Transcript saved at:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Lectura – Transcribe Your Lecture")
root.geometry("420x200")

label = tk.Label(root, text="Upload and Transcribe a Lecture Recording", font=("Helvetica", 14))
label.pack(pady=20)

upload_button = tk.Button(root, text="Select Audio File", command=select_audio, font=("Helvetica", 12))
upload_button.pack(pady=10)

root.mainloop()
