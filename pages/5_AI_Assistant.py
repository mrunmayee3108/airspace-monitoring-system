import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from agent import ask_agent

# --- ADD THIS BLOCK START ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("🚨 GEMINI_API_KEY not found! Check your .env file or Streamlit Secrets.")

st.set_page_config(
    page_title="AI Assistant · Airspace Monitor",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {
    padding-top: 0 !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
}
section[data-testid="stSidebar"] { display: none !important; }

:root {
    --bg-primary: #050a14;
    --bg-card: #0c1526;
    --accent-blue: #00d4ff;
    --accent-cyan: #00ffcc;
    --accent-red: #ff3366;
    --text-primary: #e8f4fd;
    --text-muted: #7a9bbf;
    --border: rgba(0, 212, 255, 0.15);
}

body, .stApp {
    background: var(--bg-primary) !important;
    font-family: 'Rajdhani', sans-serif;
    color: var(--text-primary);
}

/* ── NAVBAR ── */
.navbar {
    position: sticky; top: 0; z-index: 999;
    background: rgba(5,10,20,0.95); backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border); padding: 0 2.5rem;
    display: flex; align-items: center; justify-content: space-between;
    height: 64px; box-shadow: 0 4px 30px rgba(0,0,0,0.5);
    margin-left: -1rem; margin-right: -1rem;
}
.navbar-brand {
    display: flex; align-items: center; gap: 12px;
    font-family: 'Orbitron', monospace; font-weight: 700; font-size: 1.1rem;
    color: var(--accent-blue); letter-spacing: 0.05em; text-decoration: none;
}
.navbar-links { display: flex; gap: 0.25rem; align-items: center; }
a.nav-link, a.nav-link:visited {
    padding: 0.45rem 1.1rem; border-radius: 6px;
    font-family: 'Rajdhani', sans-serif; font-size: 0.9rem; font-weight: 500;
    color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em;
    border: 1px solid transparent; white-space: nowrap; text-decoration: none; transition: all 0.2s ease;
}
a.nav-link:hover { color: var(--accent-blue); border-color: var(--border); background: rgba(0,212,255,0.07); }
a.nav-link.active { color: var(--accent-blue); border-color: rgba(0,212,255,0.4); background: rgba(0,212,255,0.1); }
.nav-badge {
    display: inline-block; padding: 2px 7px; background: var(--accent-red); color: white;
    border-radius: 10px; font-size: 0.65rem; font-weight: 700; margin-left: 4px; vertical-align: middle;
}
.navbar-status { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: var(--accent-cyan); font-family: 'Orbitron', monospace; }
.status-dot { width: 6px; height: 6px; background: var(--accent-cyan); border-radius: 50%; animation: pulse 1.5s infinite; box-shadow: 0 0 6px var(--accent-cyan); }

/* ── PAGE HEADER ── */
.page-header {
    padding: 2rem 0.5rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.page-breadcrumb {
    font-size: 0.72rem; color: var(--text-muted);
    font-family: 'Orbitron', monospace; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.4rem;
}
.page-breadcrumb span { color: var(--accent-blue); }
.page-title {
    font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 700; color: var(--text-primary);
}
.page-title span { color: var(--accent-blue); text-shadow: 0 0 20px rgba(0,212,255,0.4); }

/* ── CHAT WRAPPER ── */
.chat-outer { max-width: 860px; margin: 0 auto; }

/* ── STREAMLIT CHAT MESSAGES ── */
div[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem !important;
    padding: 0.75rem 1rem !important;
}
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    border-color: rgba(0, 212, 255, 0.25) !important;
    background: rgba(0, 212, 255, 0.05) !important;
}
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    border-color: rgba(0, 255, 204, 0.15) !important;
    background: rgba(0, 255, 204, 0.03) !important;
}
div[data-testid="stChatMessageContent"] p {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    color: var(--text-primary) !important;
    line-height: 1.65 !important;
}

/* ── CHAT INPUT ── */
div[data-testid="stChatInput"] > div {
    background: var(--bg-card) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    border-radius: 12px !important;
    max-width: 860px !important;
    margin: 0.5rem auto 0 !important;
    transition: border-color 0.2s ease;
}
div[data-testid="stChatInput"] > div:focus-within {
    border-color: rgba(0, 212, 255, 0.7) !important;
    box-shadow: 0 0 16px rgba(0, 212, 255, 0.1) !important;
}
div[data-testid="stChatInput"] textarea {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    color: var(--text-primary) !important;
    background: transparent !important;
    caret-color: var(--accent-blue) !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}

/* ── SUGGESTION CHIPS ── */
.suggestions {
    display: flex; gap: 0.6rem; flex-wrap: wrap;
    margin-bottom: 1.25rem;
}
.chip {
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 20px; padding: 0.35rem 0.9rem;
    font-size: 0.8rem; color: var(--text-muted);
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 0.04em;
}
.chip:hover { color: var(--accent-blue); border-color: rgba(0,212,255,0.45); }

@keyframes pulse { 0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.5;transform:scale(0.85);} }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR 
st.markdown("""
<div class="navbar">
    <a href="/" class="navbar-brand">
        <span>✈️</span>
        <span>AIRSPACE<span style="color:#7a9bbf;font-weight:400"> </span>MONITOR</span>
        <div class="dot"></div>
    </a>
    <div class="navbar-links">
        <a href="/" class="nav-link active">Dashboard</a>
        <a href="/Airspace_Activity" class="nav-link">🌍 Airspace</a>
        <a href="/Object_Classification" class="nav-link">🛰️ Objects</a>
        <a href="/Predicted_Trajectories" class="nav-link">📡 Trajectories</a>
        <a href="/Spoofing_Detection" class="nav-link">🛸 Spoofing</a>
        <a href="/AI_Assistant" class="nav-link">🤖 AI</a>
    </div>
</div>
""", unsafe_allow_html=True)

#  PAGE HEADER 
st.markdown("""
<div class="page-header">
    <div class="page-breadcrumb">Dashboard / <span>AI Assistant</span></div>
    <div class="page-title">🤖 <span>AI</span> Assistant</div>
</div>
""", unsafe_allow_html=True)

#  CHAT 
st.markdown('<div class="chat-outer">', unsafe_allow_html=True)

st.markdown("""
<div class="suggestions">
    <div class="chip">How many anomalies are detected?</div>
    <div class="chip">What are the high risk objects?</div>
    <div class="chip">Summarize current airspace status</div>
    <div class="chip">What trajectories are flagged?</div>
</div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# Show chat history
for q, a in st.session_state.history:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(a)

# Input
user_input = st.chat_input("Ask about airspace activity, anomalies, risk levels...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        with st.spinner(""):
            answer = ask_agent(user_input, st.session_state.history)
        st.write(answer)
    st.session_state.history.append((user_input, answer))

st.markdown('</div>', unsafe_allow_html=True)
