import streamlit as st
import pandas as pd
import numpy as np
import random

# ------------------------------------------------------
# BRAND COLORS (Honeycomb Theme)
# ------------------------------------------------------
BURTS_YELLOW = "#F4C32D"
BURTS_RED = "#C51F25"
BURTS_DARK = "#4A2C2A"
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
    <div style='text-align:center; padding:18px; 
         background-color:{BURTS_YELLOW}; 
         border-radius:12px; border:3px solid {BURTS_RED};'>
        <span style='color:{BURTS_RED}; font-size:32px; font-weight:800;'>
            Burt’s Bees Trend Sensing Dashboard
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------
# MOCK TREND DATA
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
# TREND CARD (SAFE + BEAUTIFUL)
# ------------------------------------------------------
def trend_card(trend, growth, priority):
    border_color = BURTS_RED if priority == "High" else BURTS_GOLD if priority == "Medium" else BURTS_LIGHT

    # Pure HTML (no buttons inside!)
    st.markdown(
        f"""
        <div style='
            background-color:{BURTS_YELLOW};
            border:3px solid {border_color};
            border-radius:14px;
            padding:16px;
            box-shadow:0px 3px 6px rgba(0,0,0,0.12);
            text-align:center;
            min-height:150px;
        '>

            <div style='font-size:20px; font-weight:700; color:{BURTS_DARK};'>
                🍯 {trend}
            </div>

            <div style='font-size:16px; margin-top:6px; color:{BURTS_DARK};'>
                Growth: {growth}%
            </div>

            <div style='
                margin-top:10px;
                display:inline-block;
                padding:4px 14px;
                border-radius:20px;
                font-size:13px;
                font-weight:700;
                background-color:{border_color};
                color:white;
            '>
                {priority}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # SEPARATE BUTTON (critical!)
    if st.button(f"View Details: {trend}", key=f"btn_{trend}"):
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

    # 🔥 Highlight HIGH PRIORITY at the top
    high_df = df[df["Priority"] == "High"].sort_values("Growth %", ascending=False)

    if not high_df.empty:
        st.subheader("🔥 High Priority Trends (Most Important)")
        rows_hp = [high_df.iloc[i:i+3] for i in range(0, len(high_df), 3)]
        for row in rows_hp:
            cols = st.columns(3)
            for col, (_, t) in zip(cols, row.iterrows()):
                with col:
                    trend_card(t["Trend"], t["Growth %"], t["Priority"])

    # 🔼 Top Growing
    st.subheader("Top 5 Fastest Growing Trends")
    top_growing = df.sort_values("Growth %", ascending=False).head(5)
    rows = [top_growing.iloc[i:i+3] for i in range(0, len(top_growing), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, (_, t) in zip(cols, row.iterrows()):
            with col:
                trend_card(t["Trend"], t["Growth %"], t["Priority"])

    # 🔽 Top Declining
    st.subheader("Top 5 Declining Trends")
    top_declining = df.sort_values("Growth %", ascending=True).head(5)
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

    all_rows = [df.iloc[i:i+3] for i in range(0, len(df), 3)]
    for row in all_rows:
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

    insight("Why This Trend Matters", f"{selected} reflects a shift toward natural performance ingredients.")
    insight("Consumer Need", f"Consumers seek hydration, barrier repair, and clean ingredients — all tied to {selected}.")
    insight("Opportunity for Burt’s Bees", f"{selected} aligns closely with Burt’s Bees’ nature-first brand ethos.")

    st.subheader("Simulated Trend Trajectory")
    st.line_chart(np.random.randint(50, 100, size=12))
