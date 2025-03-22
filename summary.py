import os
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq

# Download NLTK resources if needed
nltk.download("punkt")
nltk.download("stopwords")

# ----------------------------
# Function to generate paragraph summary
# ----------------------------
def generate_paragraph_summary(text, max_sentences=5):
    """Generate a basic paragraph-style summary from a transcript."""
    stop_words = set(stopwords.words("english"))
    word_frequencies = {}
    sentences = sent_tokenize(text)

    for word in word_tokenize(text.lower()):
        if word.isalpha() and word not in stop_words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    if not word_frequencies:
        return "Summary could not be generated — not enough meaningful content detected."

    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    best_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(best_sentences)

    return summary

# ----------------------------
# Function to generate study tips
# ----------------------------
def generate_study_tips(transcript_text):
    lines = transcript_text.splitlines()

    test_topics = []
    assignments = []
    common_mistakes = []

    for line in lines:
        lower_line = line.lower()

        if "on the test" in lower_line or "for the exam" in lower_line:
            test_topics.append(line.strip())

        if "due" in lower_line or "assignment" in lower_line or "submit" in lower_line:
            assignments.append(line.strip())

        if "mistake" in lower_line or "commonly confused" in lower_line:
            common_mistakes.append(line.strip())

    tips = "\n📚 Study Tips\n\n"

    if test_topics:
        tips += "✅ Likely Test Topics:\n"
        tips += "\n".join(f"• {topic}" for topic in test_topics) + "\n\n"

    if assignments:
        tips += "📅 Assignments / Due Dates:\n"
        tips += "\n".join(f"• {assign}" for assign in assignments) + "\n\n"

    if common_mistakes:
        tips += "⚠️ Common Mistakes:\n"
        tips += "\n".join(f"• {mistake}" for mistake in common_mistakes) + "\n"

    if not (test_topics or assignments or common_mistakes):
        tips += "No specific tips detected — consider reviewing this lecture manually. 🧐"

    return tips.strip()

# ----------------------------
# Function to generate topic summary
# ----------------------------
def generate_topic_summary(transcript_text):
    stop_words = set(stopwords.words('english'))
    custom_ignore = {"speaker", "okay", "tips", "specific", "thing", "test", "that", "this", "what"}

    words = re.findall(r'\b[a-zA-Z]{4,}\b', transcript_text.lower())
    filtered_words = [word for word in words if word not in stop_words and word not in custom_ignore]
    word_counts = Counter(filtered_words)

    key_terms = [word for word, count in word_counts.items() if count > 1][:10]

    topic_lines = []
    for line in transcript_text.splitlines():
        if any(kw in line.lower() for kw in ["topic", "main idea", "important", "discuss", "cover", "focus"]):
            topic_lines.append(line.strip())

    summary = "\n🧵 Summary of Lecture Topics\n\n"
    summary += "\n".join(f"• {line}" for line in topic_lines) if topic_lines else "No obvious topic lines found.\n"

    summary += "\n\n📚 Key Terms Mentioned\n\n"
    summary += "\n".join(f"• {term}" for term in key_terms) if key_terms else "No strong key terms detected."

    return summary.strip()

# ----------------------------
# Script to apply summary and tips
# ----------------------------
notes_folder = "notes"
if not os.path.exists(notes_folder):
    print("❌ 'notes' folder not found. Please create a folder named 'notes' and add transcripts there.")
    exit(1)

transcripts = [f for f in os.listdir(notes_folder) if f.endswith(".txt")]

if not transcripts:
    print("❌ No transcript files found in the 'notes' folder.")
    exit(1)

print("🗂 Available transcripts:")
for idx, file in enumerate(transcripts):
    print(f"{idx + 1}. {file}")

choice = input("\n📄 Enter the number of the transcript you'd like to summarize: ").strip()

try:
    file_index = int(choice) - 1
    selected_file = transcripts[file_index]
    full_path = os.path.join(notes_folder, selected_file)

    with open(full_path, "r", encoding="utf-8") as file:
        content = file.read()

    if "🧵 Summary of Lecture Topics" in content:
        print("⚠️ This transcript already contains a summary. Skipping to avoid duplication.")
        exit(0)

    # Ask user whether to save a new file
    save_new = input("💾 Save as a new file? (y/n): ").lower().startswith("y")
    if save_new:
        output_path = os.path.join(notes_folder, selected_file.replace(".txt", "_analyzed.txt"))
    else:
        output_path = full_path

    # Generate sections
    tips = generate_study_tips(content)
    summary = generate_topic_summary(content)
    paragraph_summary = generate_paragraph_summary(content)

    with open(output_path, "a", encoding="utf-8") as file:
        file.write("\n\n" + tips)
        file.write("\n\n" + summary)
        file.write("\n\n📝 Summary Paragraph\n\n" + paragraph_summary)

    print(f"✅ Study tips and topic summary added to '{os.path.basename(output_path)}'.")

except (ValueError, IndexError):
    print("❌ Invalid selection. Please run the script again and enter a valid number.")
