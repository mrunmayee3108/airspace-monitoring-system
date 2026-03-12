import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Airspace Activity · AI Airspace Monitor",
    layout="wide",
    page_icon="✈️"
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
    background: rgba(5, 10, 20, 0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    padding: 0 2.5rem;
    display: flex; align-items: center; justify-content: space-between;
    height: 64px;
    box-shadow: 0 4px 30px rgba(0,0,0,0.5);
    margin-left: -1rem; margin-right: -1rem;
}
.navbar-brand {
    display: flex; align-items: center; gap: 12px;
    font-family: 'Orbitron', monospace; font-weight: 700; font-size: 1.1rem;
    color: var(--accent-blue); letter-spacing: 0.05em;
    text-decoration: none;
}
.navbar-links { display: flex; gap: 0.25rem; align-items: center; }
a.nav-link, a.nav-link:visited {
    padding: 0.45rem 1.1rem; border-radius: 6px;
    font-family: 'Rajdhani', sans-serif; font-size: 0.9rem; font-weight: 500;
    color: var(--text-muted); cursor: pointer; transition: all 0.2s ease;
    text-transform: uppercase; letter-spacing: 0.08em;
    border: 1px solid transparent; white-space: nowrap; text-decoration: none;
}
a.nav-link:hover { color: var(--accent-blue); border-color: var(--border); background: rgba(0,212,255,0.07); }
a.nav-link.active { color: var(--accent-blue); border-color: rgba(0,212,255,0.4); background: rgba(0,212,255,0.1); }
.nav-badge {
    display: inline-block; padding: 2px 7px;
    background: var(--accent-red); color: white;
    border-radius: 10px; font-size: 0.65rem; font-weight: 700;
    margin-left: 4px; vertical-align: middle;
}
.navbar-status {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.8rem; color: var(--accent-cyan);
    font-family: 'Orbitron', monospace;
}


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
    font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 700;
    color: var(--text-primary); letter-spacing: 0.03em;
}
.page-title span { color: var(--accent-blue); text-shadow: 0 0 20px rgba(0,212,255,0.4); }

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.25rem 1.5rem;
    position: relative; overflow: hidden;
}
.metric-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
}
.metric-label {
    font-size: 0.68rem; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.12em;
    font-family: 'Orbitron', monospace; margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Orbitron', monospace; font-size: 1.9rem; font-weight: 700;
    color: var(--accent-blue); line-height: 1;
    text-shadow: 0 0 15px rgba(0,212,255,0.35);
}
.metric-unit {
    font-size: 0.75rem; color: var(--text-muted); margin-top: 5px;
}

/* ── SECTION HEADERS ── */
.section-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 0.75rem; margin-top: 1.75rem;
}
.section-line {
    width: 3px; height: 20px;
    background: linear-gradient(180deg, var(--accent-blue), var(--accent-cyan));
    border-radius: 2px; box-shadow: 0 0 6px var(--accent-blue);
}
.section-title {
    font-family: 'Orbitron', monospace; font-size: 0.85rem; font-weight: 600;
    color: var(--text-primary); letter-spacing: 0.08em; text-transform: uppercase;
}

/* ── CHART WRAPPER ── */
.chart-wrap {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 14px; padding: 1rem;
}

/* ── FILTER PANEL ── */
.filter-panel {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 14px; padding: 1.25rem 1rem;
}
.filter-title {
    font-family: 'Orbitron', monospace; font-size: 0.68rem; font-weight: 600;
    color: var(--text-muted); letter-spacing: 0.15em; text-transform: uppercase;
    margin-bottom: 1rem; padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}

/* Slider label styling */
div[data-testid="stSlider"] label p {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.8rem !important; color: var(--text-muted) !important;
    text-transform: uppercase; letter-spacing: 0.08em;
}

@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:0.5; transform:scale(0.85); }
}
</style>
""", unsafe_allow_html=True)

#NAVBAR
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

#PAGE HEADER
st.markdown("""
<div class="page-header">
    <div class="page-breadcrumb">Dashboard / <span>Airspace Activity</span></div>
    <div class="page-title">🌍 <span>Airspace</span> Activity</div>
</div>
""", unsafe_allow_html=True)

#LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard_dataset.csv")
    df = df.dropna(subset=["latitude", "longitude"])
    df["velocity"] = df["velocity"].fillna(0).abs()
    df["geo_altitude"] = df["geo_altitude"].fillna(0)
    return df

df = load_data()

# LAYOUT
filter_col, content_col = st.columns([1, 4])

with filter_col:
    st.markdown('<div class="filter-panel"><div class="filter-title">⚙ Filters</div>', unsafe_allow_html=True)
    velocity_range = st.slider(
        "Velocity (m/s)",
        float(df["velocity"].min()), float(df["velocity"].max()),
        (float(df["velocity"].min()), float(df["velocity"].max()))
    )
    st.markdown("<br>", unsafe_allow_html=True)
    altitude_range = st.slider(
        "Altitude (m)",
        float(df["geo_altitude"].min()), float(df["geo_altitude"].max()),
        (float(df["geo_altitude"].min()), float(df["geo_altitude"].max()))
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered_df = df[
    (df["velocity"].between(*velocity_range)) &
    (df["geo_altitude"].between(*altitude_range))
]

with content_col:
    total   = len(filtered_df)
    avg_vel = round(filtered_df["velocity"].mean(), 1) if total else 0
    avg_alt = round(filtered_df["geo_altitude"].mean(), 0) if total else 0

    #METRICS
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        (m1, "Total Aircraft",    total,        "tracked objects"),
        (m2, "Avg Velocity",      avg_vel,      "m/s"),
        (m3, "Avg Altitude",      int(avg_alt), "metres"),
    ]
    for col, label, value, unit in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-unit">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

    #AIRCRAFT MAP
    st.markdown("""
    <div class="section-header">
        <div class="section-line"></div>
        <div class="section-title">Aircraft Map</div>
    </div>
    """, unsafe_allow_html=True)

    fig_map = px.scatter_mapbox(
        filtered_df, lat="latitude", lon="longitude",
        size="velocity", color="geo_altitude",
        hover_data=["velocity", "geo_altitude", "vertical_rate"],
        zoom=2, height=500, color_continuous_scale="Turbo"
    )
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False
    )
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── TRAFFIC DENSITY ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <div class="section-line"></div>
        <div class="section-title">Traffic Density Heatmap</div>
    </div>
    """, unsafe_allow_html=True)

    fig_density = px.density_mapbox(
        filtered_df, lat="latitude", lon="longitude",
        z="velocity", radius=8, zoom=2, height=460
    )
    fig_density.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_density, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    #VELOCITY VS ALTITUDE
    st.markdown("""
    <div class="section-header">
        <div class="section-line"></div>
        <div class="section-title">Velocity vs Altitude</div>
    </div>
    """, unsafe_allow_html=True)

    fig_scatter = px.scatter(
        filtered_df, x="velocity", y="geo_altitude",
        color="vertical_rate", size="velocity",
        labels={"velocity": "Velocity (m/s)", "geo_altitude": "Altitude (m)"},
        color_continuous_scale="Turbo", height=420
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(12,21,38,0.8)",
        font=dict(family="Rajdhani, sans-serif", color="#7a9bbf"),
        margin=dict(r=10, t=10, l=10, b=10)
    )
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
