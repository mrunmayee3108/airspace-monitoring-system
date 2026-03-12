import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(
    page_title="Ghost Aircraft Detection",
    page_icon="👻",
    layout="wide"
)

st.title("👻Ghost Aircraft/ADS-B Spoofing Detection")

st.markdown("""
This module identifies physically impossible aircraft behaviour which may indicate:
* ADS-B spoofing
* Fake aircraft injection
* Sensor malfunction
* Teleportation anomalies
""")

@st.cache_data
def load_data():
    return pd.read_csv("final_airspace_data.csv")

df = load_data()

df["ghost_flag"] = 0
df.loc[df["velocity"] > 1200, "ghost_flag"] = 1
df.loc[df["vertical_rate"].abs() > 100, "ghost_flag"] = 1

ghost_df = df[df["ghost_flag"] == 1]

col1, col2 = st.columns(2)
col1.metric("Total Aircraft", len(df))
col2.metric("Ghost Aircraft Detected", len(ghost_df))

st.divider()

st.subheader("Aircraft Map")

df["color"] = df["ghost_flag"].apply(
    lambda x: [255, 0, 0] if x == 1 else [0, 120, 255]
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_color="color",
    get_radius=4000
)

view_state = pdk.ViewState(
    latitude=df["latitude"].mean(),
    longitude=df["longitude"].mean(),
    zoom=3
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

st.divider()

st.subheader("Suspicious Aircraft")

if len(ghost_df) > 0:
    st.warning(f"{len(ghost_df)} suspicious aircraft detected")
    st.dataframe(
        ghost_df[
            [
                "velocity",
                "vertical_rate",
                "geo_altitude",
                "latitude",
                "longitude"
            ]
        ]
    )
else:
    st.success("No ghost aircraft detected")