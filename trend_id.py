import streamlit as st
import pandas as pd
import numpy as np
import random

# ------------------------------------------------------
# BURT'S BEES BRAND COLORS
# ------------------------------------------------------
BURTS_YELLOW = "#F4C32D"
BURTS_RED = "#C51F25"
BURTS_DARK = "#4A2C2A"
BURTS_OFFWHITE = "#FFF8E7"
BURTS_GOLD = "#DFAF2B"

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(page_title="Burt’s Bees Trend Sensing Dashboard", layout="wide")

# Initialize session state
if "selected_trend" not in st.session_state:
    st.session_state.selected_trend = None


# ------------------------------------------------------
# GLOBAL STYLING
# ------------------------------------------------------
st.markdown(f"""
    <style>

        body {{
            background-color: {BURTS_OFFWHITE};
        }}

        .header-bar {{
            background-color: {BURTS_YELLOW};
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 25px;
            border: 3px solid {BURTS_RED};
        }}

        .header-title {{
            color: {BURTS_RED};
            font-size: 32px;
            font-weight: bold;
            text-align: center;
        }}

        /* HONEYCOMB HEXAGON STYLES */
        .hex-grid {{
            display: flex;
            flex-wrap: wrap;
            width: 100%;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }}

        .hex {{
            width: 120px;
            height: 70px;
            background-color: {BURTS_YELLOW};
            position: relative;
            margin: 35px 10px;
            clip-path: polygon(
                50% 0%, 
                93% 25%, 
                93% 75%, 
                50% 100%, 
                7% 75%, 
                7% 25%
            );
            border: 3px solid {BURTS_RED};
            cursor: pointer;
            transition: transform 0.2s ease;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .hex:hover {{
            transform: scale(1.08);
        }}

        .hex p {{
            text-align: center;
            font-size: 14px;
            font-weight: bold;
            color: {BURTS_DARK};
            margin: 0;
            padding: 0 5px;
        }}

        /* Insight Cards */
        .insight-card {{
            background-color: {BURTS_YELLOW};
            border: 2px solid {BURTS_RED};
            border-radius: 14px;
            padding: 18px 22px;
            margin-top: 18px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
        }}

        .insight-header {{
            background-color: {BURTS_RED};
            color: white;
            padding: 8px 14px;
            border-radius: 10px;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 12px;
            display: inline-block;
        }}

        .insight-body {{
            color: {BURTS_DARK};
            font-size: 16px;
            line-height: 1.45;
        }}

        .insight-row {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .honey-icon {{
            font-size: 32px;
        }}

    </style>
""", unsafe_allow_html=True)


# ------------------------------------------------------
# HEADER BAR
# ------------------------------------------------------
st.markdown("""
<div class="header-bar">
    <div class="header-title">Burt’s Bees Trend Sensing Dashboard</div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------
# HELPERS
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
            "Growth %": round(random.uniform(5, 60), 2)
        })
    return pd.DataFrame(rows)


def hexagon_card(label, growth):
    """Create a clickable hexagon via HTML."""
    safe_label = label.replace(" ", "_")

    html = f"""
        /?trend={safe_label}#deepdive
            <p>{label}<br>{growth}%</p>
        </div>
    """
    return html


def render_hex_grid(df):
    html = '<div class="hex-grid">'
    for _, row in df.iterrows():
        html += hexagon_card(row["Trend"], row["Growth %"])
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_insight_card(title, body):
    st.markdown(f"""
        <div class="insight-card">
            <div class="insight-row">
                <div class="honey-icon">🍯</div>
                <div>
                    <div class="insight-header">{title}</div>
                    <div class="insight-body">{body}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------
# TABS
# ------------------------------------------------------
tabs = st.tabs([
    "Quarterly Snapshot",
    "Trend Explorer",
    "Trend Deep Dive"
])

df = generate_mock_trends()

# ------------------------------------------------------
# TAB 1 — QUARTERLY SNAPSHOT
# ------------------------------------------------------
with tabs[0]:
    st.header("Quarterly Snapshot")

    top_growing = df.sort_values("Growth %", ascending=False).head(5)
    top_declining = df.sort_values("Growth %", ascending=True).head(5)

    st.subheader("Top 5 Fastest Growing Trends")
    render_hex_grid(top_growing)

    st.subheader("Top 5 Declining Trends")
    render_hex_grid(top_declining)

# ------------------------------------------------------
# TAB 2 — TREND EXPLORER
# ------------------------------------------------------
with tabs[1]:
    st.header("Explore All Trends")
    render_hex_grid(df)


# ------------------------------------------------------
# DEEP DIVE TAB
# ------------------------------------------------------
with tabs[2]:
    st.markdown('<a name="deepdive"></a>', unsafe_allow_html=True)
    st.header("Trend Deep Dive")

    # Detect selected trend via URL param
    trend_param = st.query_params.get("trend", [None])[0]
    if trend_param:
        st.session_state.selected_trend = trend_param.replace("_", " ")

    selected = st.session_state.selected_trend or df["Trend"].iloc[0]

    st.subheader(f"Selected Trend: {selected}")

    # Insight Cards
    render_insight_card(
        "Why This Trend Matters",
        f"'{selected}' reflects a growing shift toward performance-focused natural ingredients."
    )

    render_insight_card(
        "Consumer Need",
        f"Consumers seek hydration, barrier repair, and clean ingredients — all aligned with '{selected}'."
    )

    render_insight_card(
        "Opportunity for Burt’s Bees",
        f"Strong fit for nature-forward innovation. Consider concept testing around '{selected}'."
    )

    st.subheader("Simulated Trend Trajectory")
    st.line_chart(np.random.randint(50, 100, size=12))
