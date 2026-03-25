import streamlit as st
from google import genai
import io
import os  # <--- THIS IS THE MISSING PIECE

from dotenv import load_dotenv

# 1. Page Configuration & Cyberpunk Styling
st.set_page_config(page_title="Engineer AI Pro", page_icon="🛠️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stChatInputContainer { padding-bottom: 20px; }
    .stChatMessage { border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    h1 { color: #58a6ff; font-family: 'Consolas', monospace; font-weight: bold; }
    .st-emotion-cache-16idsys p { font-size: 1.1rem; }
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Workspace
with st.sidebar:
    st.title("⚙️ DevTools")
    st.info("System: Online 🟢")
    
    # File Uploader for Engineers
    uploaded_file = st.file_uploader("Upload Code/Docs (Java, Py, TXT)", type=['java', 'py', 'txt', 'pdf'])
    
    if st.button("🗑️ Clear Terminal"):
        st.session_state.messages = []
        st.rerun()

# 3. Setup Gemini Client (Persistent)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config={'system_instruction': 'You are a Senior Lead Engineer. Use Markdown for code blocks. Be concise and technical.'}
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Main UI
st.title("🛠️ Engineer's AI Hub")
st.caption("v2.0 | Multi-Modal Technical Assistant")

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Input Logic
if prompt := st.chat_input("Enter technical query..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare Content (Include File if uploaded)
    content_list = [prompt]
    if uploaded_file:
        # Read the file content
        file_bytes = uploaded_file.getvalue()
        file_text = file_bytes.decode("utf-8")
        content_list.insert(0, f"CONTEXT FROM FILE ({uploaded_file.name}):\n{file_text}")

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Compiling response..."):
            try:
                response = st.session_state.chat.send_message(content_list)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Execution Error: {e}")