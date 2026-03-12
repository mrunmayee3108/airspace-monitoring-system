import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(
    page_title="Spoofing Detection · Airspace Monitor",
    page_icon="👻",
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

/* INFO BANNER */
.info-banner {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-blue);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.7;
}
.info-banner strong { color: var(--accent-blue); font-family: 'Orbitron', monospace; font-size: 0.75rem; letter-spacing: 0.08em; display: block; margin-bottom: 0.5rem; }
.info-tags { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.75rem; }
.info-tag {
    background: rgba(0,212,255,0.07); border: 1px solid rgba(0,212,255,0.2);
    border-radius: 20px; padding: 0.2rem 0.8rem;
    font-size: 0.75rem; color: var(--text-muted);
    font-family: 'Rajdhani', sans-serif; letter-spacing: 0.04em;
}

/* METRIC CARDS */
.metrics-row { display: flex; gap: 1rem; margin-bottom: 1.75rem; flex-wrap: wrap; }
.metric-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1.1rem 1.4rem; flex: 1; min-width: 150px; position: relative; overflow: hidden; }
.metric-card::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent-blue), transparent); }
.metric-card.red::after { background: linear-gradient(90deg, transparent, var(--accent-red), transparent); }
.metric-label { font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.12em; font-family: 'Orbitron', monospace; margin-bottom: 0.4rem; }
.metric-value { font-family: 'Orbitron', monospace; font-size: 1.7rem; font-weight: 700; color: var(--accent-blue); line-height: 1; text-shadow: 0 0 15px rgba(0,212,255,0.3); }
.metric-value.red { color: var(--accent-red); text-shadow: 0 0 15px rgba(255,51,102,0.3); }
.metric-unit { font-size: 0.72rem; color: var(--text-muted); margin-top: 4px; }

/* SECTION */
.section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem; margin-top: 1.75rem; }
.section-line { width: 3px; height: 20px; background: linear-gradient(180deg, var(--accent-blue), var(--accent-cyan)); border-radius: 2px; box-shadow: 0 0 6px var(--accent-blue); }
.section-title { font-family: 'Orbitron', monospace; font-size: 0.85rem; font-weight: 600; color: var(--text-primary); letter-spacing: 0.08em; text-transform: uppercase; }

/* CHART WRAP */
.chart-wrap { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 1rem; margin-bottom: 0.5rem; overflow: hidden; }

/* ALERT BANNER */
.alert-danger {
    background: rgba(255, 51, 102, 0.08);
    border: 1px solid rgba(255, 51, 102, 0.3);
    border-left: 3px solid var(--accent-red);
    border-radius: 10px;
    padding: 0.9rem 1.25rem;
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    color: var(--accent-red);
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 10px;
}
.alert-safe {
    background: rgba(0, 255, 204, 0.06);
    border: 1px solid rgba(0, 255, 204, 0.25);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 10px;
    padding: 0.9rem 1.25rem;
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    color: var(--accent-cyan);
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 10px;
}

/* Override Streamlit warning/success */
div[data-testid="stAlert"] { display: none !important; }

/* Dataframe */
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

@keyframes pulse { 0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.5;transform:scale(0.85);} }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────────────────
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

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-breadcrumb">Dashboard / <span>Alerts</span></div>
    <div class="page-title">👻 Ghost Aircraft / <span>ADS-B Spoofing</span> Detection</div>
</div>
""", unsafe_allow_html=True)

# ── INFO BANNER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-banner">
    <strong>⚠ DETECTION MODULE</strong>
    This module identifies physically impossible aircraft behaviour which may indicate spoofing or sensor faults.
    <div class="info-tags">
        <div class="info-tag">🛑 ADS-B Spoofing</div>
        <div class="info-tag">👻 Fake Aircraft Injection</div>
        <div class="info-tag">⚡ Sensor Malfunction</div>
        <div class="info-tag">🌀 Teleportation Anomalies</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("final_airspace_data.csv")

df = load_data()

df["ghost_flag"] = 0
df.loc[df["velocity"] > 1200, "ghost_flag"] = 1
df.loc[df["vertical_rate"].abs() > 100, "ghost_flag"] = 1

ghost_df = df[df["ghost_flag"] == 1]
ghost_pct = round(len(ghost_df) / len(df) * 100, 1) if len(df) > 0 else 0

# ── METRICS ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="metrics-row">
    <div class="metric-card">
        <div class="metric-label">Total Aircraft</div>
        <div class="metric-value">{len(df)}</div>
        <div class="metric-unit">tracked objects</div>
    </div>
    <div class="metric-card red">
        <div class="metric-label">Ghost Aircraft</div>
        <div class="metric-value red">{len(ghost_df)}</div>
        <div class="metric-unit">suspicious detections</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Normal Aircraft</div>
        <div class="metric-value">{len(df) - len(ghost_df)}</div>
        <div class="metric-unit">verified normal</div>
    </div>
    <div class="metric-card red">
        <div class="metric-label">Ghost Ratio</div>
        <div class="metric-value red">{ghost_pct}%</div>
        <div class="metric-unit">of total traffic</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MAP ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header"><div class="section-line"></div><div class="section-title">Aircraft Map — Ghost Detection</div></div>
""", unsafe_allow_html=True)

df["color"] = df["ghost_flag"].apply(
    lambda x: [255, 51, 102, 200] if x == 1 else [0, 212, 255, 140]
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_color="color",
    get_radius=4000,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=df["latitude"].mean(),
    longitude=df["longitude"].mean(),
    zoom=3
)

tooltip = {
    "html": "<b>Velocity:</b> {velocity} m/s<br/><b>Vertical Rate:</b> {vertical_rate} m/s<br/><b>Altitude:</b> {geo_altitude} m",
    "style": {"backgroundColor": "#0c1526", "color": "#e8f4fd", "fontFamily": "Rajdhani", "border": "1px solid rgba(0,212,255,0.3)", "borderRadius": "8px"}
}

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/dark-v10"
    ),
    height=520
)
st.markdown('</div>', unsafe_allow_html=True)

# ── SUSPICIOUS AIRCRAFT TABLE ─────────────────────────────────────────────────
st.markdown("""
<div class="section-header"><div class="section-line"></div><div class="section-title">Suspicious Aircraft Log</div></div>
""", unsafe_allow_html=True)

if len(ghost_df) > 0:
    st.markdown(f'<div class="alert-danger">🚨 &nbsp; {len(ghost_df)} SUSPICIOUS AIRCRAFT DETECTED — Immediate review recommended</div>', unsafe_allow_html=True)
    display_cols = [c for c in ["velocity", "vertical_rate", "geo_altitude", "latitude", "longitude", "risk_level", "anomaly"] if c in ghost_df.columns]
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.dataframe(
        ghost_df[display_cols].reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="alert-safe">✅ &nbsp; NO GHOST AIRCRAFT DETECTED — All traffic within normal parameters</div>', unsafe_allow_html=True)
