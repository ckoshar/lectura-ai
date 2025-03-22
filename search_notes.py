import os
import glob

try:
    from fuzzywuzzy import fuzz
except ImportError:
    print("❌ Please install fuzzywuzzy first: pip install fuzzywuzzy[speedup]")
    exit(1)

def highlight_match(line, query):
    """Highlight matching part of the line."""
    start = line.lower().find(query.lower())
    if start == -1:
        return line  # fallback: no match found
    end = start + len(query)
    return (
        line[:start]
        + "\033[93m" + line[start:end] + "\033[0m"  # yellow highlight
        + line[end:]
    )

def search_transcripts(query, folder="notes", threshold=60):
    results = []

    if not os.path.exists(folder):
        print(f"❌ Folder '{folder}' not found. Please create it and add some transcripts.")
        return []

    for filepath in glob.glob(f"{folder}/*.txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            if fuzz.partial_ratio(query.lower(), line.lower()) >= threshold:
                highlighted = highlight_match(line.strip(), query)
                results.append((os.path.basename(filepath), highlighted))

    return results


if __name__ == "__main__":
    print("\n🧠 Lectura: Transcript Search\n")
    query = input("🔍 What would you like to search for in your notes? ")

    matches = search_transcripts(query)

    if matches:
        print("\n📌 Search Results:")
        for file, line in matches:
            print(f"📄 {file} → {line}")
    else:
        print("❌ No relevant results found.")
        available = glob.glob("notes/*.txt")
        if available:
            print("\n📁 Available transcripts:")
            for f in available:
                print(" -", os.path.basename(f))
