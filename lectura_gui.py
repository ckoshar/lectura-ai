import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from config import (
    PROJECT_ROOT,
    DATA_DIR,
    RECORDINGS_DIR,
    TRANSCRIPTS_DIR,
    SUMMARIES_DIR,
    LOGS_DIR
)

class LecturaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lectura - AI Lecture Notes")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create buttons
        self.record_button = ttk.Button(
            self.main_frame,
            text="Record Lecture",
            command=self.record_lecture
        )
        self.record_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.transcribe_button = ttk.Button(
            self.main_frame,
            text="Transcribe Recording",
            command=self.transcribe_recording
        )
        self.transcribe_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.summarize_button = ttk.Button(
            self.main_frame,
            text="Summarize Transcript",
            command=self.summarize_transcript
        )
        self.summarize_button.grid(row=2, column=0, padx=5, pady=5)
        
        # Create text area for displaying results
        self.text_area = tk.Text(self.main_frame, wrap=tk.WORD, width=80, height=30)
        self.text_area.grid(row=3, column=0, padx=5, pady=5)
        
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.main_frame,
            orient=tk.VERTICAL,
            command=self.text_area.yview
        )
        self.scrollbar.grid(row=3, column=1, sticky=(tk.N, tk.S))
        self.text_area['yscrollcommand'] = self.scrollbar.set
    
    def record_lecture(self):
        """Start recording a lecture."""
        # TODO: Implement recording functionality
        self.text_area.insert(tk.END, "Recording started...\n")
    
    def transcribe_recording(self):
        """Transcribe a recorded lecture."""
        file_path = filedialog.askopenfilename(
            initialdir=RECORDINGS_DIR,
            title="Select Recording",
            filetypes=(("Audio files", "*.wav *.mp3"), ("All files", "*.*"))
        )
        if file_path:
            self.text_area.insert(tk.END, f"Transcribing {file_path}...\n")
            # TODO: Implement transcription functionality
    
    def summarize_transcript(self):
        """Summarize a transcript."""
        file_path = filedialog.askopenfilename(
            initialdir=TRANSCRIPTS_DIR,
            title="Select Transcript",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            self.text_area.insert(tk.END, f"Summarizing {file_path}...\n")
            # TODO: Implement summarization functionality

def main():
    root = tk.Tk()
    app = LecturaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
