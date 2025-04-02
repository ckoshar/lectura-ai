from transformers import pipeline

# Load once and reuse — this may take a few seconds on first run
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def generate_summary(text):
    # Limit input to 4000 characters (about 800 words) to avoid model cutoff
    text = text.strip().replace("\n", " ")
    text = text[:4000]

    try:
        summary_output = summarizer(
            text,
            max_length=200,
            min_length=60,
            do_sample=False
        )
        summary = summary_output[0]['summary_text']
    except Exception as e:
        summary = f"[Summary generation failed: {e}]"

    study_tips = (
        "\n\nStudy Tips:\n"
        "- Review the key ideas mentioned in the summary.\n"
        "- Create flashcards based on core concepts.\n"
        "- Reflect on what the summary implies for your class."
    )

    return "Summary:\n" + summary + study_tips

def append_summary_to_file(transcript_path):
    try:
        with open(transcript_path, "r+", encoding="utf-8") as f:
            content = f.read()
            summary = generate_summary(content)
            f.write("\n\n---\n\n" + summary)
    except Exception as e:
        raise RuntimeError(f"Failed to append summary: {str(e)}")
