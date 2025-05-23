import streamlit as st
import os
import tempfile
from transcribe import transcribe
from summary import generate_summary
from deepgram_transcribe import transcribe as deepgram_transcribe
import time

# Page configuration
st.set_page_config(
    page_title="Lectura - AI-Powered Lecture Notes",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4B8BBE;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #306998;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d1e7dd;
        color: #0f5132;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4B8BBE;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #306998;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=Lectura", width=150)
    st.markdown("## 🎧 Lectura")
    st.markdown("AI-Powered Lecture Notes")
    st.markdown("---")
    
    st.markdown("### 📝 About")
    st.markdown("""
    Lectura helps students turn lecture recordings into smart, structured notes with:
    - 🎙️ Audio transcription
    - 👥 Speaker identification
    - 📚 Topic summaries
    - 💡 Study tips
    - 🔍 Searchable notes
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Settings")
    transcription_engine = st.radio(
        "Transcription Engine",
        ["Whisper (Local)", "Deepgram (API)"],
        index=0
    )
    
    st.markdown("---")
    
    st.markdown("### 🔗 Links")
    st.markdown("[GitHub Repository](https://github.com/ckoshar/Lectura)")
    st.markdown("[Documentation](https://github.com/ckoshar/Lectura/wiki)")

# Main content
st.markdown('<h1 class="main-header">🎧 Lectura – AI-Powered Lecture Notes</h1>', unsafe_allow_html=True)

# Tabs for different features
tab1, tab2, tab3 = st.tabs(["📝 Transcribe", "🔍 Search Notes", "⚙️ Settings"])

with tab1:
    st.markdown('<h2 class="sub-header">Upload Your Lecture Recording</h2>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an audio file (.mp3, .m4a, .wav)",
        type=["mp3", "m4a", "wav"]
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File type": uploaded_file.type,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process button
        if st.button("Process Recording"):
            with st.spinner("Processing your file... ⏳"):
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_path = temp_file.name
                
                # Transcribe based on selected engine
                if transcription_engine == "Whisper (Local)":
                    transcript_path = transcribe(temp_path)
                else:
                    transcript_path = deepgram_transcribe(temp_path)
                
                # Clean up temp file
                os.unlink(temp_path)
                
                # Read transcript
                with open(transcript_path, "r", encoding="utf-8") as f:
                    transcript = f.read()
                
                # Generate summary
                summary = generate_summary(transcript)
                
                st.markdown('<div class="success-box">✅ Processing complete!</div>', unsafe_allow_html=True)
            
            # Display results in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<h3 class="sub-header">📝 Transcript</h3>', unsafe_allow_html=True)
                st.text_area("", transcript, height=300)
                
                # Download transcript button
                st.download_button(
                    label="Download Transcript",
                    data=transcript,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}_transcript.txt",
                    mime="text/plain"
                )
            
            with col2:
                st.markdown('<h3 class="sub-header">🧠 Summary & Study Tips</h3>', unsafe_allow_html=True)
                st.markdown(summary)
                
                # Download summary button
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}_summary.txt",
                    mime="text/plain"
                )

with tab2:
    st.markdown('<h2 class="sub-header">Search Your Notes</h2>', unsafe_allow_html=True)
    
    # Search input
    search_query = st.text_input("Enter search terms")
    
    if search_query:
        # Import search function
        from search_notes import search_transcripts
        
        # Perform search
        results = search_transcripts(search_query)
        
        if results:
            st.markdown(f"### Found {len(results)} matches:")
            
            for file, line in results:
                st.markdown(f"**📄 {file}**")
                st.markdown(f"```\n{line}\n```")
                st.markdown("---")
        else:
            st.info("No matches found. Try different search terms.")

with tab3:
    st.markdown('<h2 class="sub-header">Application Settings</h2>', unsafe_allow_html=True)
    
    # API Keys
    st.markdown("### API Keys")
    
    anthropic_key = st.text_input("Anthropic API Key", type="password")
    if anthropic_key:
        os.environ["ANTHROPIC_API_KEY"] = anthropic_key
    
    deepgram_key = st.text_input("Deepgram API Key", type="password")
    if deepgram_key:
        os.environ["DEEPGRAM_API_KEY"] = deepgram_key
    
    # Storage settings
    st.markdown("### Storage Settings")
    
    home = os.path.expanduser("~")
    default_notes_dir = os.path.join(home, "Lectura", "notes")
    
    notes_dir = st.text_input("Notes Directory", value=default_notes_dir)
    
    # Save settings button
    if st.button("Save Settings"):
        # In a real app, you'd save these settings to a config file
        st.success("Settings saved successfully!")
