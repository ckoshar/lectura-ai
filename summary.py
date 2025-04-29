import os
import anthropic
from error_handler import (
    SummarizationError, 
    APIError, 
    FileError, 
    handle_error, 
    logger
)

# Initialize Anthropic client
try:
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
except Exception as e:
    logger.error(f"Failed to initialize Anthropic client: {str(e)}")
    client = None

def generate_summary(text):
    """
    Generate a summary of the given text using Claude Sonnet 3.7.
    
    Args:
        text: The text to summarize
        
    Returns:
        A string containing the summary and study tips
    """
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
            max_tokens=500,
            temperature=0,
            system="You are a helpful assistant that creates concise summaries of lecture transcripts. Focus on the key points, concepts, and main ideas.",
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize the following lecture transcript, highlighting the main points and key concepts:\n\n{text}"
                }
            ]
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

def append_summary_to_file(transcript_path):
    """
    Append a summary to a transcript file.
    
    Args:
        transcript_path: Path to the transcript file
        
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
        summary = generate_summary(content)
        
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
        print("Usage: python summary.py <transcript_file_path>")
        sys.exit(1)
    
    transcript_path = sys.argv[1]
    try:
        append_summary_to_file(transcript_path)
        print(f"Summary appended to: {transcript_path}")
    except Exception as e:
        error_message = handle_error(e, "summary.py")
        print(f"Error: {error_message}")
        sys.exit(1)
