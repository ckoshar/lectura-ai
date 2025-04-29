import streamlit as st
import os
import tempfile
import time
import datetime
from pathlib import Path

# Import Lectura modules
from transcribe import transcribe
from summary import generate_summary
from deepgram_transcribe import transcribe as deepgram_transcribe
from search_notes import search_transcripts
from mac_recorder import start_recording, check_sox_installation

# Page configuration
st.set_page_config(
    page_title="Lectura Demo",
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
    .feature-card {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
    st.markdown("## 🎧 Lectura Demo")
    st.markdown("AI-Powered Lecture Notes")
    st.markdown("---")
    
    st.markdown("### 📝 About")
    st.markdown("""
    This demo showcases all features of Lectura:
    - 🎙️ Audio recording
    - 📝 Transcription
    - 👥 Speaker identification
    - 📚 Summaries
    - 💡 Study tips
    - 🔍 Search
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
st.markdown('<h1 class="main-header">🎧 Lectura Demo</h1>', unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="info-box">
    <h3>Welcome to the Lectura Demo!</h3>
    <p>This demo showcases all the features of Lectura, an AI-powered lecture notes application.</p>
    <p>Use the tabs below to explore different features:</p>
</div>
""", unsafe_allow_html=True)

# Tabs for different features
tab1, tab2, tab3, tab4 = st.tabs(["🎙️ Record", "📝 Transcribe", "🔍 Search", "⚙️ Settings"])

# Record Tab
with tab1:
    st.markdown('<h2 class="sub-header">Record a Lecture</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🎙️ Record Audio</h3>
        <p>Record audio directly from your microphone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if sox is installed
    if not check_sox_installation():
        st.error("Sox is not installed. Please install it with: `brew install sox`")
    else:
        if st.button("Start Recording"):
            with st.spinner("Recording in progress... Press Ctrl+C in the terminal to stop."):
                # This would normally open a terminal window for recording
                # For demo purposes, we'll simulate recording
                st.info("In a real implementation, this would open a terminal window for recording.")
                st.info("For now, we'll simulate recording for 5 seconds.")
                
                # Simulate recording
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.05)
                    progress_bar.progress(i + 1)
                
                st.success("Recording complete!")
                
                # Simulate a recorded file
                demo_file = "demo_recording.m4a"
                st.download_button(
                    label="Download Demo Recording",
                    data=b"Demo audio data",
                    file_name=demo_file,
                    mime="audio/m4a"
                )

# Transcribe Tab
with tab2:
    st.markdown('<h2 class="sub-header">Transcribe Audio</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>📝 Transcribe Audio</h3>
        <p>Upload an audio file to transcribe it.</p>
    </div>
    """, unsafe_allow_html=True)
    
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
        if st.button("Transcribe"):
            with st.spinner("Transcribing your file... ⏳"):
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
                
                st.markdown('<div class="success-box">✅ Transcription complete!</div>', unsafe_allow_html=True)
            
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

# Search Tab
with tab3:
    st.markdown('<h2 class="sub-header">Search Your Notes</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 Search Notes</h3>
        <p>Search through your saved transcripts.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search input
    search_query = st.text_input("Enter search terms")
    
    if search_query:
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

# Settings Tab
with tab4:
    st.markdown('<h2 class="sub-header">Application Settings</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>⚙️ Settings</h3>
        <p>Configure application settings.</p>
    </div>
    """, unsafe_allow_html=True)
    
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

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Lectura Demo | Created with ❤️ by Carter Koshar</p>
    <p>Version 1.0.0</p>
</div>
""", unsafe_allow_html=True) 