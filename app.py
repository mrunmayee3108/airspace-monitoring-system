import streamlit as st

st.set_page_config(
    page_title="AI Airspace Monitoring System",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {padding-top: 0 !important; padding-left: 0 !important; padding-right: 0 !important; max-width: 100% !important;}
section[data-testid="stSidebar"] {display: none;}

:root {
    --bg-primary: #050a14;
    --bg-secondary: #090f1e;
    --bg-card: #0c1526;
    --accent-blue: #00d4ff;
    --accent-cyan: #00ffcc;
    --accent-red: #ff3366;
    --accent-amber: #ffaa00;
    --text-primary: #e8f4fd;
    --text-muted: #7a9bbf;
    --border: rgba(0, 212, 255, 0.15);
    --glow: 0 0 20px rgba(0, 212, 255, 0.3);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body, .stApp {
    background: var(--bg-primary) !important;
    font-family: 'Rajdhani', sans-serif;
    color: var(--text-primary);
}

.navbar {
    position: sticky; top: 0; z-index: 999;
    background: rgba(5, 10, 20, 0.92);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    padding: 0 2.5rem;
    display: flex; align-items: center; justify-content: space-between;
    height: 64px;
    box-shadow: 0 4px 30px rgba(0,0,0,0.5);
}
.navbar-brand {
    display: flex; align-items: center; gap: 12px;
    font-family: 'Orbitron', monospace; font-weight: 700; font-size: 1.1rem;
    color: var(--accent-blue); letter-spacing: 0.05em; text-shadow: var(--glow);
    text-decoration: none;
}
.navbar-brand .dot {
    width: 8px; height: 8px; background: var(--accent-cyan);
    border-radius: 50%; animation: pulse 2s infinite; box-shadow: 0 0 8px var(--accent-cyan);
}
.navbar-links { display: flex; gap: 0.25rem; align-items: center; }
a.nav-link, a.nav-link:visited {
    padding: 0.45rem 1.1rem; border-radius: 6px;
    font-family: 'Rajdhani', sans-serif; font-size: 0.9rem; font-weight: 500;
    color: var(--text-muted); transition: all 0.2s ease;
    text-transform: uppercase; letter-spacing: 0.08em;
    border: 1px solid transparent; white-space: nowrap; text-decoration: none;
}
a.nav-link:hover { color: var(--accent-blue); border-color: var(--border); background: rgba(0,212,255,0.07); }
a.nav-link.active { color: var(--accent-blue); border-color: rgba(0,212,255,0.4); background: rgba(0,212,255,0.1); }
.nav-badge {
    display: inline-block; padding: 2px 7px; background: var(--accent-red); color: white;
    border-radius: 10px; font-size: 0.65rem; font-weight: 700; margin-left: 4px;
    vertical-align: middle; animation: blink 1.5s infinite;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.navbar-status {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.8rem; color: var(--accent-cyan); font-family: 'Orbitron', monospace;
}
.status-dot {
    width: 6px; height: 6px; background: var(--accent-cyan);
    border-radius: 50%; animation: pulse 1.5s infinite; box-shadow: 0 0 6px var(--accent-cyan);
}
@keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(0.85); } }

.hero {
    position: relative; padding: 5rem 3rem 4rem; overflow: hidden;
    background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,212,255,0.08) 0%, transparent 60%),
                linear-gradient(180deg, #050a14 0%, #07101f 100%);
    border-bottom: 1px solid var(--border);
}
.hero-grid {
    position: absolute; inset: 0;
    background-image: linear-gradient(rgba(0,212,255,0.04) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(0,212,255,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 0%, transparent 70%);
}
.hero-tag {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3);
    border-radius: 20px; padding: 0.3rem 1rem; font-size: 0.75rem;
    color: var(--accent-blue); font-family: 'Orbitron', monospace;
    letter-spacing: 0.1em; margin-bottom: 1.5rem; text-transform: uppercase;
}
.hero-title {
    font-family: 'Orbitron', monospace; font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 900; color: var(--text-primary); line-height: 1.15;
    margin-bottom: 1rem; letter-spacing: -0.01em;
}
.hero-title span { color: var(--accent-blue); text-shadow: 0 0 30px rgba(0,212,255,0.5); }
.hero-sub { font-size: 1.15rem; color: var(--text-muted); max-width: 560px; line-height: 1.7; margin-bottom: 2.5rem; }
.hero-stats { display: flex; gap: 2.5rem; flex-wrap: wrap; }
.stat { display: flex; flex-direction: column; }
.stat-value { font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 700; color: var(--accent-blue); line-height: 1; text-shadow: 0 0 15px rgba(0,212,255,0.4); }
.stat-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }

.section { padding: 3rem 3rem; }
.section-header { display: flex; align-items: center; gap: 14px; margin-bottom: 2rem; }
.section-line { width: 3px; height: 24px; background: linear-gradient(180deg, var(--accent-blue), var(--accent-cyan)); border-radius: 2px; box-shadow: 0 0 8px var(--accent-blue); }
.section-title { font-family: 'Orbitron', monospace; font-size: 1rem; font-weight: 600; color: var(--text-primary); letter-spacing: 0.08em; text-transform: uppercase; }

.cards-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.25rem; max-width: 1100px; }
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 1.75rem; position: relative; overflow: hidden; transition: all 0.3s ease; }
.card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent-blue), transparent); opacity: 0; transition: opacity 0.3s; }
.card:hover { border-color: rgba(0,212,255,0.35); transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 20px rgba(0,212,255,0.08); }
.card:hover::before { opacity: 1; }
.card-icon { font-size: 1.8rem; margin-bottom: 0.75rem; display: block; }
.card-title { font-family: 'Orbitron', monospace; font-size: 0.95rem; font-weight: 600; color: var(--text-primary); letter-spacing: 0.05em; margin-bottom: 0.5rem; }
.card-desc { font-size: 0.9rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1.25rem; }
.card-btn { display: inline-flex; align-items: center; gap: 8px; padding: 0.5rem 1.25rem; border: 1px solid rgba(0,212,255,0.4); border-radius: 7px; background: rgba(0,212,255,0.07); color: var(--accent-blue) !important; font-family: 'Rajdhani', sans-serif; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; cursor: pointer; transition: all 0.2s ease; text-decoration: none !important; }
.card-btn:hover { background: rgba(0,212,255,0.18); box-shadow: 0 0 15px rgba(0,212,255,0.2); }
.card-btn-red { border-color: rgba(255,51,102,0.4) !important; background: rgba(255,51,102,0.07) !important; color: var(--accent-red) !important; }
.card-btn-red:hover { background: rgba(255,51,102,0.18) !important; }

.footer { border-top: 1px solid var(--border); padding: 1.5rem 3rem; display: flex; align-items: center; justify-content: space-between; background: rgba(9,15,30,0.5); }
.footer-text { font-size: 0.8rem; color: var(--text-muted); font-family: 'Orbitron', monospace; letter-spacing: 0.05em; }
.footer-links { display: flex; gap: 1.5rem; }
.footer-link { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; cursor: pointer; transition: color 0.2s; }
.footer-link:hover { color: var(--accent-blue); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
    <a href="/" class="navbar-brand">
        <span>✈️</span>
        <span>AIRSPACE<span style="color:#7a9bbf;font-weight:400"> / </span>MONITOR</span>
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

st.markdown("""
<div class="hero">
    <div class="hero-grid"></div>
    <div style="position:relative; z-index:1;">
        <div class="hero-tag">
            <div class="status-dot"></div>
            AI-Powered · Real-Time Monitoring
        </div>
        <div class="hero-title">AI <span>Airspace</span><br>Monitoring System</div>
        <div class="hero-sub">Advanced real-time surveillance and classification of airspace activity. Detect anomalies, track trajectories, and respond to threats instantly.</div>
        <div class="hero-stats">
            <div class="stat"><div class="stat-value">247</div><div class="stat-label">Active Aircraft</div></div>
            <div class="stat"><div class="stat-value">3</div><div class="stat-label">Active Alerts</div></div>
            <div class="stat"><div class="stat-value">99.8%</div><div class="stat-label">System Uptime</div></div>
            <div class="stat"><div class="stat-value">14ms</div><div class="stat-label">Avg. Latency</div></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
    <div class="section-header">
        <div class="section-line"></div>
        <div class="section-title">Dashboard Modules</div>
    </div>
    <div class="cards-grid">
        <div class="card">
            <span class="card-icon">🌍</span>
            <div class="card-title">Airspace Activity</div>
            <div class="card-desc">View aircraft locations, traffic density, and flight behavior across monitored zones in real time.</div>
            <a href="/Airspace_Activity" class="card-btn">→ Open Airspace Activity</a>
        </div>
        <div class="card">
            <span class="card-icon">🛰️</span>
            <div class="card-title">Object Classification</div>
            <div class="card-desc">AI-powered identification and classification of all objects detected within the monitored airspace.</div>
            <a href="/Object_Classification" class="card-btn">→ Open Classification</a>
        </div>
        <div class="card">
            <span class="card-icon">📡</span>
            <div class="card-title">Predicted Trajectories</div>
            <div class="card-desc">Machine learning models predict and visualize future aircraft movement paths and potential conflicts.</div>
            <a href="/Predicted_Trajectories" class="card-btn">→ Open Trajectories</a>
        </div>
        <div class="card">
            <span class="card-icon">🛸</span>
            <div class="card-title">Spoofing Detection</div>
            <div class="card-desc">Detect ghost aircraft, ADS-B spoofing, and physically impossible flight behaviour in real time.</div>
            <a href="/Spoofing_Detection" class="card-btn card-btn-red">→ Open Spoofing Detection</a>
        </div>
        <div class="card">
            <span class="card-icon">🤖</span>
            <div class="card-title">AI Assistant</div>
            <div class="card-desc">Conversational AI that analyzes airspace data and answers operational questions.</div>
            <a href="/AI_Assistant" class="card-btn">→ Open AI Assistant</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div class="footer-text">© 2025 AI AIRSPACE MONITORING SYSTEM</div>
    <div class="footer-links">
        <div class="footer-link">Docs</div>
        <div class="footer-link">API</div>
        <div class="footer-link">Support</div>
        <div class="footer-link">Status</div>
    </div>
</div>
""", unsafe_allow_html=True)
