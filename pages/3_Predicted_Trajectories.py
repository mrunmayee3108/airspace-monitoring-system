import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Predicted Trajectories · Airspace Monitor",
    layout="wide",
    page_icon="📡"
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

/* METRIC CARDS */
.metrics-row { display: flex; gap: 1rem; margin-bottom: 1.75rem; flex-wrap: wrap; }
.metric-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1.1rem 1.4rem; flex: 1; min-width: 150px; position: relative; overflow: hidden; }
.metric-card::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent-blue), transparent); }
.metric-card.red::after { background: linear-gradient(90deg, transparent, var(--accent-red), transparent); }
.metric-card.amber::after { background: linear-gradient(90deg, transparent, var(--accent-amber), transparent); }
.metric-card.cyan::after { background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent); }
.metric-label { font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.12em; font-family: 'Orbitron', monospace; margin-bottom: 0.4rem; }
.metric-value { font-family: 'Orbitron', monospace; font-size: 1.7rem; font-weight: 700; color: var(--accent-blue); line-height: 1; text-shadow: 0 0 15px rgba(0,212,255,0.3); }
.metric-value.red { color: var(--accent-red); text-shadow: 0 0 15px rgba(255,51,102,0.3); }
.metric-value.amber { color: var(--accent-amber); text-shadow: 0 0 15px rgba(255,170,0,0.3); }
.metric-value.cyan { color: var(--accent-cyan); text-shadow: 0 0 15px rgba(0,255,204,0.3); }
.metric-unit { font-size: 0.72rem; color: var(--text-muted); margin-top: 4px; }

/* SECTION */
.section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem; margin-top: 1.75rem; }
.section-line { width: 3px; height: 20px; background: linear-gradient(180deg, var(--accent-blue), var(--accent-cyan)); border-radius: 2px; box-shadow: 0 0 6px var(--accent-blue); }
.section-title { font-family: 'Orbitron', monospace; font-size: 0.85rem; font-weight: 600; color: var(--text-primary); letter-spacing: 0.08em; text-transform: uppercase; }
.section-sub { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.75rem; }

/* CHART WRAP */
.chart-wrap { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 1rem; margin-bottom: 0.5rem; }

/* FILTER PANEL */
.filter-panel { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 1.25rem 1rem; }
.filter-title { font-family: 'Orbitron', monospace; font-size: 0.68rem; font-weight: 600; color: var(--text-muted); letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 1rem; padding-bottom: 0.6rem; border-bottom: 1px solid var(--border); }

/* RISK BADGE */
.badge { display: inline-block; padding: 2px 10px; border-radius: 10px; font-size: 0.72rem; font-family: 'Orbitron', monospace; font-weight: 600; letter-spacing: 0.08em; }
.badge-high { background: rgba(255,51,102,0.15); color: var(--accent-red); border: 1px solid rgba(255,51,102,0.3); }
.badge-medium { background: rgba(255,170,0,0.15); color: var(--accent-amber); border: 1px solid rgba(255,170,0,0.3); }
.badge-low { background: rgba(0,255,204,0.1); color: var(--accent-cyan); border: 1px solid rgba(0,255,204,0.2); }

div[data-testid="stSlider"] label p { font-family: 'Rajdhani', sans-serif !important; font-size: 0.8rem !important; color: var(--text-muted) !important; text-transform: uppercase; letter-spacing: 0.08em; }

@keyframes pulse { 0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.5;transform:scale(0.85);} }
</style>
""", unsafe_allow_html=True)

#  NAVBAR 
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
    <div class="page-breadcrumb">Dashboard / <span>Predicted Trajectories</span></div>
    <div class="page-title">📡 <span>Predicted</span> Trajectories</div>
</div>
""", unsafe_allow_html=True)

#  LOAD DATA + MODELS 
@st.cache_data
def load_data():
    df = pd.read_csv("final_airspace_data.csv")
    df = df.dropna(subset=["latitude", "longitude", "pred_latitude", "pred_longitude"])
    return df

@st.cache_resource
def load_models():
    try:
        lat_model = joblib.load("trajectory_lat_model.pkl")
        lon_model = joblib.load("trajectory_lon_model.pkl")
        return lat_model, lon_model
    except Exception:
        return None, None

df = load_data()
lat_model, lon_model = load_models()

#  LAYOUT 
filter_col, content_col = st.columns([1, 4])

with filter_col:
    st.markdown('<div class="filter-panel"><div class="filter-title">⚙ Filters</div>', unsafe_allow_html=True)

    risk_filter = st.multiselect(
        "Risk Level",
        options=["HIGH", "MEDIUM", "LOW"],
        default=["HIGH", "MEDIUM", "LOW"]
    )

    if "velocity" in df.columns:
        vel_range = st.slider(
            "Velocity (m/s)",
            float(df["velocity"].min()), float(df["velocity"].max()),
            (float(df["velocity"].min()), float(df["velocity"].max()))
        )
    else:
        vel_range = None

    show_actual = st.checkbox("Show actual path", value=True)
    show_predicted = st.checkbox("Show predicted path", value=True)
    show_arrows = st.checkbox("Show direction arrows", value=True)

    st.markdown('</div>', unsafe_allow_html=True)

#  APPLY FILTERS 
filtered = df.copy()
if "risk_level" in df.columns:
    filtered = filtered[filtered["risk_level"].str.upper().isin(risk_filter)]
if vel_range and "velocity" in df.columns:
    filtered = filtered[filtered["velocity"].between(*vel_range)]

with content_col:

    #  METRICS 
    total = len(filtered)
    high  = (filtered["risk_level"].str.upper() == "HIGH").sum()   if "risk_level" in filtered.columns else 0
    med   = (filtered["risk_level"].str.upper() == "MEDIUM").sum() if "risk_level" in filtered.columns else 0
    low   = (filtered["risk_level"].str.upper() == "LOW").sum()    if "risk_level" in filtered.columns else 0

    # compute average trajectory error
    filtered["traj_error"] = np.sqrt(
        (filtered["pred_latitude"]  - filtered["latitude"])**2 +
        (filtered["pred_longitude"] - filtered["longitude"])**2
    )
    avg_error = round(filtered["traj_error"].mean() * 111, 2)  # degrees → ~km

    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card">
            <div class="metric-label">Total Aircraft</div>
            <div class="metric-value">{total}</div>
            <div class="metric-unit">tracked</div>
        </div>
        <div class="metric-card red">
            <div class="metric-label">High Risk</div>
            <div class="metric-value red">{high}</div>
            <div class="metric-unit">objects</div>
        </div>
        <div class="metric-card amber">
            <div class="metric-label">Medium Risk</div>
            <div class="metric-value amber">{med}</div>
            <div class="metric-unit">objects</div>
        </div>
        <div class="metric-card cyan">
            <div class="metric-label">Low Risk</div>
            <div class="metric-value cyan">{low}</div>
            <div class="metric-unit">objects</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Avg Pred Error</div>
            <div class="metric-value">{avg_error}</div>
            <div class="metric-unit">km approx</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # VIZ 1: ACTUAL vs PREDICTED POSITIONS ON MAP 
    st.markdown("""
    <div class="section-header"><div class="section-line"></div><div class="section-title">Actual vs Predicted Positions</div></div>
    <div class="section-sub">Blue = actual position · Orange = model-predicted next position · Lines show displacement</div>
    """, unsafe_allow_html=True)

    fig_map = go.Figure()

    if show_actual:
        fig_map.add_trace(go.Scattermapbox(
            lat=filtered["latitude"],
            lon=filtered["longitude"],
            mode="markers",
            marker=dict(size=6, color="#00d4ff", opacity=0.8),
            name="Actual Position",
            hovertemplate="<b>Actual</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>"
        ))

    if show_predicted:
        fig_map.add_trace(go.Scattermapbox(
            lat=filtered["pred_latitude"],
            lon=filtered["pred_longitude"],
            mode="markers",
            marker=dict(size=6, color="#ff9900", opacity=0.8),
            name="Predicted Position",
            hovertemplate="<b>Predicted</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>"
        ))

    if show_arrows:
        # Draw lines connecting actual → predicted for a sample of points
        sample = filtered.sample(min(300, len(filtered)), random_state=42)
        for _, row in sample.iterrows():
            fig_map.add_trace(go.Scattermapbox(
                lat=[row["latitude"], row["pred_latitude"]],
                lon=[row["longitude"], row["pred_longitude"]],
                mode="lines",
                line=dict(width=1, color="rgba(255,153,0,0.35)"),
                showlegend=False,
                hoverinfo="skip"
            ))

    fig_map.update_layout(
        mapbox=dict(style="carto-darkmatter", zoom=2,
                    center=dict(lat=filtered["latitude"].mean(), lon=filtered["longitude"].mean())),
        margin=dict(r=0, t=0, l=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#7a9bbf", family="Rajdhani"), bgcolor="rgba(12,21,38,0.8)",
                    bordercolor="rgba(0,212,255,0.2)", borderwidth=1),
        height=520
    )

    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── VIZ 2: TRAJECTORY ERROR BY RISK LEVEL ────────────────────────────────
    st.markdown("""
    <div class="section-header"><div class="section-line"></div><div class="section-title">Prediction Error by Risk Level</div></div>
    <div class="section-sub">How far off the model's prediction is, grouped by risk category</div>
    """, unsafe_allow_html=True)

    color_map = {"HIGH": "#ff3366", "MEDIUM": "#ffaa00", "LOW": "#00ffcc"}

    if "risk_level" in filtered.columns:
        fig_box = px.box(
            filtered, x="risk_level", y="traj_error",
            color="risk_level",
            color_discrete_map={k: v for k, v in color_map.items()},
            labels={"traj_error": "Prediction Error (degrees)", "risk_level": "Risk Level"},
            height=380,
            category_orders={"risk_level": ["HIGH", "MEDIUM", "LOW"]}
        )
        fig_box.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(12,21,38,0.6)",
            font=dict(family="Rajdhani", color="#7a9bbf"),
            margin=dict(r=10, t=10, l=10, b=10),
            showlegend=False,
            xaxis=dict(gridcolor="rgba(0,212,255,0.07)"),
            yaxis=dict(gridcolor="rgba(0,212,255,0.07)")
        )
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    #  VIZ 3: VELOCITY vs TRAJECTORY ERROR 
    st.markdown("""
    <div class="section-header"><div class="section-line"></div><div class="section-title">Velocity vs Prediction Error</div></div>
    <div class="section-sub">Faster aircraft tend to have larger trajectory prediction errors</div>
    """, unsafe_allow_html=True)

    if "velocity" in filtered.columns:
        fig_scatter = px.scatter(
            filtered.sample(min(1000, len(filtered)), random_state=1),
            x="velocity", y="traj_error",
            color="risk_level" if "risk_level" in filtered.columns else None,
            color_discrete_map=color_map,
            labels={"velocity": "Velocity (m/s)", "traj_error": "Prediction Error (deg)"},
            opacity=0.7, height=380
        )
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(12,21,38,0.6)",
            font=dict(family="Rajdhani", color="#7a9bbf"),
            margin=dict(r=10, t=10, l=10, b=10),
            legend=dict(font=dict(color="#7a9bbf"), bgcolor="rgba(12,21,38,0.8)",
                        bordercolor="rgba(0,212,255,0.2)", borderwidth=1),
            xaxis=dict(gridcolor="rgba(0,212,255,0.07)"),
            yaxis=dict(gridcolor="rgba(0,212,255,0.07)")
        )
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    #  VIZ 4: ALTITUDE CHANGE vs VERTICAL RATE
    st.markdown("""
    <div class="section-header"><div class="section-line"></div><div class="section-title">Altitude Change vs Vertical Rate</div></div>
    <div class="section-sub">Sudden altitude changes combined with high vertical rate are strong anomaly indicators</div>
    """, unsafe_allow_html=True)

    if "altitude_change" in filtered.columns and "vertical_rate" in filtered.columns:
        fig_alt = px.scatter(
            filtered.sample(min(1000, len(filtered)), random_state=2),
            x="altitude_change", y="vertical_rate",
            color="risk_level" if "risk_level" in filtered.columns else None,
            color_discrete_map=color_map,
            labels={"altitude_change": "Altitude Change (m)", "vertical_rate": "Vertical Rate (m/s)"},
            opacity=0.7, height=380
        )
        fig_alt.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(12,21,38,0.6)",
            font=dict(family="Rajdhani", color="#7a9bbf"),
            margin=dict(r=10, t=10, l=10, b=10),
            legend=dict(font=dict(color="#7a9bbf"), bgcolor="rgba(12,21,38,0.8)",
                        bordercolor="rgba(0,212,255,0.2)", borderwidth=1),
            xaxis=dict(gridcolor="rgba(0,212,255,0.07)"),
            yaxis=dict(gridcolor="rgba(0,212,255,0.07)")
        )
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_alt, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    #  VIZ 5: TOP HIGH-RISK AIRCRAFT TABLE 
    st.markdown("""
    <div class="section-header"><div class="section-line"></div><div class="section-title">Top High-Risk Aircraft</div></div>
    <div class="section-sub">Aircraft with the highest risk scores and prediction errors</div>
    """, unsafe_allow_html=True)

    if "risk_score" in filtered.columns:
        top = filtered.sort_values("risk_score", ascending=False).head(10)
        display_cols = [c for c in ["latitude", "longitude", "velocity", "geo_altitude",
                                     "vertical_rate", "risk_score", "risk_level", "traj_error"] if c in top.columns]
        top_display = top[display_cols].reset_index(drop=True)
        top_display.columns = [c.replace("_", " ").title() for c in display_cols]

        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.dataframe(
            top_display,
            use_container_width=True,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
