import streamlit as st
import pandas as pd
import numpy as np
import random

# ------------------------------------------------------
# BRAND COLORS
# ------------------------------------------------------
BURTS_YELLOW = "#F4C32D"
BURTS_RED = "#C51F25"
BURTS_DARK = "#4A2C2A"
BURTS_OFFWHITE = "#FFF8E7"
BURTS_GOLD = "#DFAF2B"
BURTS_LIGHT = "#FFEFAE"

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
    <div style="
        background-color:{BURTS_YELLOW};
        padding:20px;
        border-radius:12px;
        border:3px solid {BURTS_RED};
        text-align:center;
        margin-bottom:25px;
    ">
        <span style="color:{BURTS_RED}; font-size:32px; font-weight:800;">
            Burt’s Bees Trend Sensing Dashboard
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------
# DUMMY DATA
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
# TREND CARD (safe + works in Streamlit)
# ------------------------------------------------------
def trend_card(label, growth, priority):
    colors = {
        "High": BURTS_RED,
        "Medium": BURTS_GOLD,
        "Low": BURTS_LIGHT
    }
    border_color = colors[priority]

    card_html = f"""
    <div style="
        background-color:{BURTS_YELLOW};
        border:3px solid {border_color};
        border-radius:12px;
        padding:18px;
        text-align:center;
        box-shadow:0px 4px 8px rgba(0,0,0,0.10);
    ">
        <div style="font-size:20px; font-weight:700; color:{BURTS_DARK};">
            🍯 {label}
        </div>

        <div style="font-size:16px; margin-top:8px; color:{BURTS_DARK};">
            Growth: {growth}%
        </div>

        <div style="
            margin-top:10px;
            display:inline-block;
            background-color:{border_color};
            padding:4px 12px;
            border-radius:20px;
            color:white;
            font-size:12px;
            font-weight:600;
        ">
            {priority}
        </div>
    </div>
    """

    # Render
    st.markdown(card_html, unsafe_allow_html=True)

    # Button below card (Streamlit-safe way of clicking)
    if st.button(f"View Details: {label}", key=label):
        st.session_state.selected_trend = label
        st.experimental_rerun()


# ------------------------------------------------------
# INSIGHT CARD
# ------------------------------------------------------
def insight_card(title, body):
    st.markdown(
        f"""
        <div style="
            background-color:{BURTS_YELLOW};
            border:2px solid {BURTS_RED};
            padding:16px;
            border-radius:12px;
            margin-top:15px;
            box-shadow:0px 3px 6px rgba(0,0,0,0.10);
        ">
            <div style="
                background-color:{BURTS_RED};
                color:white;
                padding:6px 12px;
                display:inline-block;
                border-radius:8px;
                font-weight:700;
                font-size:18px;
                margin-bottom:8px;
            ">
                {title}
            </div>

            <div style="font-size:16px; color:{BURTS_DARK}; line-height:1.4;">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


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

    st.subheader("Top 5 Fastest Growing Trends")
    rows = [top_growing.iloc[i:i+3] for i in range(0, len(top_growing), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, (_, trend) in zip(cols, row.iterrows()):
            with col:
                trend_card(trend["Trend"], trend["Growth %"], trend["Priority"])

    st.subheader("Top 5 Declining Trends")
    rows = [top_declining.iloc[i:i+3] for i in range(0, len(top_declining), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, (_, trend) in zip(cols, row.iterrows()):
            with col:
                trend_card(trend["Trend"], trend["Growth %"], trend["Priority"])


# ------------------------------------------------------
# TAB 2 — Trend Explorer
# ------------------------------------------------------
with tabs[1]:
    st.header("Explore All Trends")

    rows = [df.iloc[i:i+3] for i in range(0, len(df), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, (_, trend) in zip(cols, row.iterrows()):
            with col:
                trend_card(trend["Trend"], trend["Growth %"], trend["Priority"])


# ------------------------------------------------------
# TAB 3 — Trend Deep Dive
# ------------------------------------------------------
with tabs[2]:
    st.header("Trend Deep Dive")

    selected = st.session_state.selected_trend or df["Trend"].iloc[0]
    st.subheader(f"Selected Trend: {selected}")

    insight_card(
        "Why This Trend Matters",
        f"'{selected}' aligns with shifts toward natural ingredient-led performance and skin wellness."
    )

    insight_card(
        "Consumer Need",
        f"Consumers prioritize hydration, repair, and simplicity—key drivers behind the '{selected}' trend."
    )

    insight_card(
        "Opportunity for Burt’s Bees",
        f"'{selected}' fits Burt’s Bees’ nature-first portfolio. Consider limited editions, flavor stories, or format innovation."
    )

    st.subheader("Simulated Trend Trajectory")
    st.line_chart(np.random.randint(50, 100, size=12))
