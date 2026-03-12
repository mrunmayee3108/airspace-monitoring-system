import streamlit as st
import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.models import load_model

st.set_page_config(
    page_title="Object Classification · Airspace Monitor",
    page_icon="🛰️",
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
    --accent-amber: #ffaa00;
    --text-primary: #e8f4fd;
    --text-muted: #7a9bbf;
    --border: rgba(0, 212, 255, 0.15);
}
body, .stApp { background: var(--bg-primary) !important; font-family: 'Rajdhani', sans-serif; color: var(--text-primary); }

/* NAVBAR */
.navbar {
    position: sticky; top: 0; z-index: 999;
    background: rgba(5,10,20,0.95); backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border); padding: 0 2.5rem;
    display: flex; align-items: center; justify-content: space-between;
    height: 64px; box-shadow: 0 4px 30px rgba(0,0,0,0.5);
    margin-left: -1rem; margin-right: -1rem;
}
.navbar-brand { display: flex; align-items: center; gap: 12px; font-family: 'Orbitron', monospace; font-weight: 700; font-size: 1.1rem; color: var(--accent-blue); letter-spacing: 0.05em; text-decoration: none; }
.navbar-links { display: flex; gap: 0.25rem; align-items: center; }
a.nav-link, a.nav-link:visited { padding: 0.45rem 1.1rem; border-radius: 6px; font-family: 'Rajdhani', sans-serif; font-size: 0.9rem; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; border: 1px solid transparent; white-space: nowrap; text-decoration: none; transition: all 0.2s ease; }
a.nav-link:hover { color: var(--accent-blue); border-color: var(--border); background: rgba(0,212,255,0.07); }
a.nav-link.active { color: var(--accent-blue); border-color: rgba(0,212,255,0.4); background: rgba(0,212,255,0.1); }
.nav-badge { display: inline-block; padding: 2px 7px; background: var(--accent-red); color: white; border-radius: 10px; font-size: 0.65rem; font-weight: 700; margin-left: 4px; vertical-align: middle; }
.navbar-status { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: var(--accent-cyan); font-family: 'Orbitron', monospace; }
.status-dot { width: 6px; height: 6px; background: var(--accent-cyan); border-radius: 50%; animation: pulse 1.5s infinite; box-shadow: 0 0 6px var(--accent-cyan); }

/* PAGE HEADER */
.page-header { padding: 2rem 0.5rem 1.5rem; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; }
.page-breadcrumb { font-size: 0.72rem; color: var(--text-muted); font-family: 'Orbitron', monospace; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.4rem; }
.page-breadcrumb span { color: var(--accent-blue); }
.page-title { font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 700; color: var(--text-primary); }
.page-title span { color: var(--accent-blue); text-shadow: 0 0 20px rgba(0,212,255,0.4); }

/* UPLOAD ZONE */
.upload-hint {
    font-size: 0.88rem; color: var(--text-muted);
    margin-bottom: 1rem; font-family: 'Rajdhani', sans-serif;
}

/* Streamlit file uploader */
div[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed rgba(0,212,255,0.3) !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
}
div[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,212,255,0.6) !important;
}
div[data-testid="stFileUploader"] label {
    color: var(--text-muted) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
    text-transform: uppercase; letter-spacing: 0.08em;
}

/* RESULT CARD */
.result-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 14px; padding: 1.5rem; position: relative; overflow: hidden;
}
.result-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
}

/* METRIC CARDS */
.metric-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1.1rem 1.4rem; position: relative; overflow: hidden; margin-bottom: 0.75rem; }
.metric-card::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent-blue), transparent); }
.metric-label { font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.12em; font-family: 'Orbitron', monospace; margin-bottom: 0.4rem; }
.metric-value { font-family: 'Orbitron', monospace; font-size: 1.7rem; font-weight: 700; color: var(--accent-blue); line-height: 1; text-shadow: 0 0 15px rgba(0,212,255,0.3); }
.metric-unit { font-size: 0.72rem; color: var(--text-muted); margin-top: 4px; }

/* CONFIDENCE BAR */
.conf-bar-wrap { margin-top: 1rem; }
.conf-bar-label { font-size: 0.72rem; color: var(--text-muted); font-family: 'Orbitron', monospace; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.4rem; }
.conf-bar-bg { background: rgba(0,212,255,0.08); border-radius: 20px; height: 10px; overflow: hidden; border: 1px solid rgba(0,212,255,0.15); }
.conf-bar-fill { height: 100%; border-radius: 20px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)); box-shadow: 0 0 8px rgba(0,212,255,0.4); transition: width 0.5s ease; }

/* ALERT BANNERS */
.alert-danger { background: rgba(255,51,102,0.08); border: 1px solid rgba(255,51,102,0.3); border-left: 3px solid var(--accent-red); border-radius: 10px; padding: 1rem 1.25rem; font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; color: var(--text-primary); line-height: 1.6; margin-top: 1rem; }
.alert-danger strong { color: var(--accent-red); font-family: 'Orbitron', monospace; font-size: 0.75rem; letter-spacing: 0.08em; display: block; margin-bottom: 0.3rem; }
.alert-safe { background: rgba(0,255,204,0.06); border: 1px solid rgba(0,255,204,0.25); border-left: 3px solid var(--accent-cyan); border-radius: 10px; padding: 1rem 1.25rem; font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; color: var(--text-primary); line-height: 1.6; margin-top: 1rem; }
.alert-safe strong { color: var(--accent-cyan); font-family: 'Orbitron', monospace; font-size: 0.75rem; letter-spacing: 0.08em; display: block; margin-bottom: 0.3rem; }

/* SECTION */
.section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem; margin-top: 1.75rem; }
.section-line { width: 3px; height: 20px; background: linear-gradient(180deg, var(--accent-blue), var(--accent-cyan)); border-radius: 2px; box-shadow: 0 0 6px var(--accent-blue); }
.section-title { font-family: 'Orbitron', monospace; font-size: 0.85rem; font-weight: 600; color: var(--text-primary); letter-spacing: 0.08em; text-transform: uppercase; }

/* INFO CARD */
.info-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 1.5rem; }
.info-text { font-size: 0.95rem; color: var(--text-muted); line-height: 1.75; }
.info-tags { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 1rem; }
.info-tag { background: rgba(0,212,255,0.07); border: 1px solid rgba(0,212,255,0.2); border-radius: 20px; padding: 0.3rem 0.9rem; font-size: 0.8rem; color: var(--text-muted); font-family: 'Rajdhani', sans-serif; }

/* Image display */
div[data-testid="stImage"] img { border-radius: 10px; border: 1px solid var(--border); }

@keyframes pulse { 0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.5;transform:scale(0.85);} }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <a href="/" class="navbar-brand">
        <span>✈️</span>
        <span>AIRSPACE<span style="color:#7a9bbf;font-weight:400"> </span>MONITOR</span>
        <div class="status-dot"></div>
    </a>
    <div class="navbar-links">
        <a href="/" class="nav-link">Dashboard</a>
        <a href="/Airspace_Activity" class="nav-link">🌍 Airspace</a>
        <a href="/Object_Classification" class="nav-link active">🛰️ Objects</a>
        <a href="/Predicted_Trajectories" class="nav-link">📡 Trajectories</a>
        <a href="/Spoofing_Detection" class="nav-link">🛸 Spoofing</a>
        <a href="/AI_Assistant" class="nav-link">🤖 AI</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-breadcrumb">Dashboard / <span>Object Classification</span></div>
    <div class="page-title">🛰️ <span>Object</span> Classification</div>
</div>
""", unsafe_allow_html=True)

# ── LOAD MODEL ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_ai_model():
    return load_model("airspace_classifier.h5")

model = load_ai_model()
classes = ["aeroplane", "bird", "drone"]

# ── UPLOAD ────────────────────────────────────────────────────────────────────
st.markdown('<div class="upload-hint">Upload an aerial image to classify objects in monitored airspace — JPG, JPEG or PNG supported.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload aerial image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded_file is None:
    st.markdown("""
    <div class="alert-safe" style="margin-top:0;">
        <strong>📡 AWAITING INPUT</strong>
        No image uploaded yet. Upload an aerial image of an aircraft, bird, or drone to begin classification.
    </div>
    """, unsafe_allow_html=True)

else:
    image = Image.open(uploaded_file).convert("RGB")

    # Prediction
    img = np.array(image)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction    = model.predict(img)
    predicted_class = classes[np.argmax(prediction)]
    confidence    = float(np.max(prediction) * 100)

    # ── TWO COLUMN LAYOUT ─────────────────────────────────────────────────────
    img_col, result_col = st.columns([1, 1], gap="large")

    with img_col:
        st.markdown("""
        <div class="section-header">
            <div class="section-line"></div>
            <div class="section-title">Uploaded Image</div>
        </div>
        """, unsafe_allow_html=True)
        st.image(image, use_column_width=True)

    with result_col:
        st.markdown("""
        <div class="section-header">
            <div class="section-line"></div>
            <div class="section-title">Detection Result</div>
        </div>
        """, unsafe_allow_html=True)

        # Object type card
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Detected Object</div>
            <div class="metric-value">{predicted_class.upper()}</div>
            <div class="metric-unit">CNN classification output</div>
        </div>
        """, unsafe_allow_html=True)

        # Confidence card with bar
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Confidence Score</div>
            <div class="metric-value">{confidence:.1f}%</div>
            <div class="conf-bar-wrap">
                <div class="conf-bar-bg">
                    <div class="conf-bar-fill" style="width:{min(confidence,100):.1f}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Airspace alert
        if predicted_class == "drone":
            st.markdown("""
            <div class="alert-danger">
                <strong>⚠ AIRSPACE ALERT — UNAUTHORIZED DRONE</strong>
                Unauthorized drone detected in monitored airspace.
                Immediate operator review recommended. Log and escalate to control.
            </div>
            """, unsafe_allow_html=True)

        elif predicted_class == "aeroplane":
            st.markdown("""
            <div class="alert-safe">
                <strong>✈ AUTHORIZED — COMMERCIAL AIRCRAFT</strong>
                Commercial aircraft detected and classified as an authorized aerial entity.
                No immediate action required.
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="alert-safe">
                <strong>🐦 NON-THREAT — BIOLOGICAL OBJECT</strong>
                Bird detected in airspace. Classified as a non-threat biological object.
                No action required.
            </div>
            """, unsafe_allow_html=True)

# ── SYSTEM OVERVIEW ───────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-line"></div>
    <div class="section-title">AI System Overview</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <div class="info-text">
        This module uses a <b style="color:#00d4ff;">Convolutional Neural Network (CNN)</b> trained on aerial imagery
        to automatically classify flying objects detected in monitored airspace.
        The model analyzes visual features and categorizes objects into threat and non-threat groups,
        providing automated alerts to operators when unauthorized objects are detected.
    </div>
    <div class="info-tags">
        <div class="info-tag">✈️ Aircraft / Aeroplanes</div>
        <div class="info-tag">🐦 Birds</div>
        <div class="info-tag">🚁 Drones (UAV)</div>
        <div class="info-tag">CNN · 224×224 Input</div>
        <div class="info-tag">Real-Time Inference</div>
    </div>
</div>
""", unsafe_allow_html=True)