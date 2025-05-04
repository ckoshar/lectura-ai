import os
import anthropic
from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from utils.error_handler import (
    SummarizationError, 
    APIError, 
    FileError, 
    handle_error, 
    logger
)
from config import TRANSCRIPTS_DIR, SUMMARIES_DIR

# Initialize Anthropic client
try:
    client = anthropic.Client(api_key=os.environ.get("ANTHROPIC_API_KEY"))
except Exception as e:
    logger.error(f"Failed to initialize Anthropic client: {str(e)}")
    client = None

# Initialize T5 summarizer
try:
    logger.info("Loading T5 summarization model")
    summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
except Exception as e:
    logger.error(f"Failed to initialize T5 summarizer: {str(e)}")
    summarizer = None

def generate_local_summary(text):
    """
    Generate a summary using T5 model.
    
    Args:
        text: The text to summarize
        
    Returns:
        A string containing the summary and study tips
    """
    try:
        if summarizer is None:
            raise SummarizationError("T5 summarizer not initialized")
            
        logger.info("Generating summary with T5 model")
        
        # Split text into chunks if too long (T5 has token limits)
        max_chunk_length = 512
        chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
        
        summaries = []
        for chunk in chunks:
            # Generate summary for each chunk
            summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        
        # Combine summaries
        combined_summary = " ".join(summaries)
        
        study_tips = (
            "\n\nStudy Tips:\n"
            "- Review the key ideas mentioned in the summary.\n"
            "- Create flashcards based on core concepts.\n"
            "- Reflect on what the summary implies for your class."
        )

        return "Local Summary:\n" + combined_summary + study_tips
    except Exception as e:
        logger.error(f"Local summary generation failed: {str(e)}")
        raise SummarizationError(f"Failed to generate local summary: {str(e)}")

def generate_summary(text, use_local=False):
    """
    Generate a summary of the given text.
    
    Args:
        text: The text to summarize
        use_local: If True, use local T5 model instead of Claude
        
    Returns:
        A string containing the summary and study tips
    """
    if use_local:
        return generate_local_summary(text)
    
    # Check if client is initialized
    if client is None:
        raise APIError("Anthropic client not initialized. Please set ANTHROPIC_API_KEY environment variable.")
    
    # Limit input to 4000 characters (about 800 words) to avoid model cutoff
    text = text.strip().replace("\n", " ")
    text = text[:4000]

    try:
        logger.info("Generating summary with Claude Sonnet 3.7")
        # Use Claude Sonnet 3.7 for summarization
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[{
                "role": "user",
                "content": f"Please summarize the following lecture transcript, highlighting the main points and key concepts:\n\n{text}"
            }],
            max_tokens=500,
            temperature=0,
            system="You are a helpful assistant that creates concise summaries of lecture transcripts. Focus on the key points, concepts, and main ideas."
        )
        summary = message.content[0].text
        logger.info("Summary generated successfully")
    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}")
        raise SummarizationError(f"Failed to generate summary: {str(e)}")

    study_tips = (
        "\n\nStudy Tips:\n"
        "- Review the key ideas mentioned in the summary.\n"
        "- Create flashcards based on core concepts.\n"
        "- Reflect on what the summary implies for your class."
    )

    return "Summary:\n" + summary + study_tips

def append_summary_to_file(transcript_path, use_local=False):
    """
    Append a summary to a transcript file.
    
    Args:
        transcript_path: Path to the transcript file
        use_local: If True, use local T5 model instead of Claude
        
    Raises:
        FileError: If the transcript file cannot be read or written
        SummarizationError: If summary generation fails
    """
    try:
        # Check if file exists
        if not os.path.exists(transcript_path):
            raise FileError(f"Transcript file not found: {transcript_path}")
        
        logger.info(f"Reading transcript from {transcript_path}")
        with open(transcript_path, "r+", encoding="utf-8") as f:
            content = f.read()
            
        logger.info("Generating summary")
        summary = generate_summary(content, use_local)
        
        logger.info(f"Appending summary to {transcript_path}")
        with open(transcript_path, "a", encoding="utf-8") as f:
            f.write("\n\n---\n\n" + summary)
            
        logger.info("Summary appended successfully")
    except FileError as e:
        # Re-raise file errors
        raise
    except SummarizationError as e:
        # Re-raise summarization errors
        raise
    except Exception as e:
        # Wrap other exceptions
        raise RuntimeError(f"Failed to append summary: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python summary.py <transcript_file_path> [--local]")
        sys.exit(1)
    
    transcript_path = sys.argv[1]
    use_local = "--local" in sys.argv
    
    try:
        append_summary_to_file(transcript_path, use_local)
        print(f"Summary appended to: {transcript_path}")
    except Exception as e:
        error_message = handle_error(e, "summary.py")
        print(f"Error: {error_message}")
        sys.exit(1)
