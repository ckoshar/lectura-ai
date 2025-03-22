# Lectura 🧠🎧

Lectura is an AI-powered study tool that helps students turn lecture recordings into smart, structured notes — complete with transcriptions, speaker labeling, topic summaries, and study tips.

---

##  Features

-  Audio Transcription  
  Convert `.m4a` or `.wav` lecture recordings into clean, readable text.

-  Speaker Identification  
  Automatically detect and label different speakers in the lecture.

-  Topic Summary  
  Paragraph-style summary of key topics covered in the lecture.

-  Study Tips  
  Extracts potential test topics, assignments, and common mistakes.

-  Searchable Notes  
  Search across your saved transcripts for specific terms or questions.

---

##  Project StWhere transcripts and summaries are saved
├── transcribe.py         # Records audio, transcribes, identifies speakers
├── summary.py            # Analyzes transcript and adds study tips & summary
├── search_notes.py       # Tool to search across all saved transcripts
├── venv/                 # Python virtual environment (not tracked by Git)

---

##  How to Use

1. Clone the repo:
   git clone https://github.com/ckoshar/Lectura.git
   cd Lectura

2. Set up the environment:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Place your audio file (e.g. lecture1.m4a) in the root folder.
e
4. Set up Hugging Face token with
  export HUGGINGFACE_TOKEN=hf_your_token_here

5. Run the transcription:
   python transcribe.py

6. Run the analysis + summary:
   python summary.py

---

## NOTE To use speaker identification, create a free Hugging Face token and paste it in step 4

## Target Audience

Lectura is designed for:
- University and high school students
- Students with learning differences (ADHD, dyslexia, etc.)
- Tutors, peer mentors, and educators

---

## Future Roadmap

- Voice-powered Q&A quiz mode
- Web-based interface (GUI)
- Flashcard generator
- AI-powered search assistant
