import streamlit as st
import pandas as pd
import numpy as np
import random

# ------------------------------------------------------
# BRAND COLORS (used only for emojis & headers)
# ------------------------------------------------------
BURTS_RED = "#C51F25"

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(page_title="Burt’s Bees Trend Sensing Dashboard", layout="wide")

if "selected_trend" not in st.session_state:
    st.session_state.selected_trend = None


# ------------------------------------------------------
# HEADER
# ------------------------------------------------------
st.markdown(
    f"""
    <h1 style="text-align:center; color:{BURTS_RED};">
        Burt’s Bees Trend Sensing Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------
# MOCK DATA
# ------------------------------------------------------
def generate_mock_trends():
    priorities = ["High", "Medium", "Low"]
    trends = [
        "Ceramides", "Honey Gloss", "Barrier Repair",
        "Scalp Health", "Hydrating Mists", "Vegan Wax Balms",
        "Botanical Fragrances", "Niacinamide Blends",
        "Dewy Finish", "Ginger Extract", "Glow Sticks",
        "AHA Body Care"
    ]
    rows = []
    for t in trends:
        rows.append({
            "Trend": t,
            "Priority": random.choice(priorities),
            "Growth %": round(random.uniform(-20, 60), 2)
        })
    return pd.DataFrame(rows)

df = generate_mock_trends()


# ------------------------------------------------------
# SIMPLE STREAMLIT TREND CARD (NO HTML)
# ------------------------------------------------------
def trend_card(trend, growth, priority):
    card = st.container()
    with card:
        st.subheader(f"🍯 {trend}")
        st.write(f"**Growth:** {growth}%")
        st.write(f"**Priority:** {priority}")

        if st.button(f"View Details", key=f"{trend}_button"):
            st.session_state.selected_trend = trend
            st.experimental_rerun()


# ------------------------------------------------------
# INSIGHT CARD
# ------------------------------------------------------
def insight(title, text):
    st.markdown(f"### {title}")
    st.write(text)


# ------------------------------------------------------
# TABS
# ------------------------------------------------------
tabs = st.tabs(["Quarterly Snapshot", "Trend Explorer", "Trend Deep Dive"])


# ------------------------------------------------------
# TAB 1 — Quarterly Snapshot
# ------------------------------------------------------
with tabs[0]:
    st.header("Quarterly Snapshot")

    top_growing = df.sort_values("Growth %", ascending=False).head(5)
    top_declining = df.sort_values("Growth %", ascending=True).head(5)

    # Top 5 Growing
    st.subheader("Top 5 Fastest Growing Trends")
    rows = [top_growing.iloc[i:i+3] for i in range(0, len(top_growing), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, (_, t) in zip(cols, row.iterrows()):
            with col:
                trend_card(t["Trend"], t["Growth %"], t["Priority"])

    # Top 5 Declining
    st.subheader("Top 5 Declining Trends")
    rows = [top_declining.iloc[i:i+3] for i in range(0, len(top_declining), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, (_, t) in zip(cols, row.iterrows()):
            with col:
                trend_card(t["Trend"], t["Growth %"], t["Priority"])


# ------------------------------------------------------
# TAB 2 — Trend Explorer
# ------------------------------------------------------
with tabs[1]:
    st.header("Explore All Trends")

    rows = [df.iloc[i:i+3] for i in range(0, len(df), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, (_, t) in zip(cols, row.iterrows()):
            with col:
                trend_card(t["Trend"], t["Growth %"], t["Priority"])


# ------------------------------------------------------
# TAB 3 — Trend Deep Dive
# ------------------------------------------------------
with tabs[2]:
    st.header("Trend Deep Dive")

    selected = st.session_state.selected_trend or df["Trend"].iloc[0]
    st.subheader(f"Selected Trend: {selected}")

    insight(
        "Why This Trend Matters",
        f"'{selected}' is driven by consumer interest in natural, results-focused ingredients."
    )

    insight(
        "Consumer Need",
        f"This trend aligns with hydration, barrier repair, and clean ingredient preferences."
    )

    insight(
        "Opportunity for Burt’s Bees",
        f"This trend connects strongly to Burt’s Bees’ nature-first positioning."
    )

    st.subheader("Simulated Trend Trajectory")
    st.line_chart(np.random.randint(50, 100, size=12))
