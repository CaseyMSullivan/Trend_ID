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

if "selected_trend" not in st.session_state:
    st.session_state.selected_trend = None


# ------------------------------------------------------
# GLOBAL CSS (clean + simple)
# ------------------------------------------------------
st.markdown(f"""
    <style>
        body {{
            background-color: {BURTS_OFFWHITE};
        }}

        /* Header */
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

        /* Trend Cards Grid */
        .card-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
        }}

        .trend-card {{
            background-color: {BURTS_YELLOW};
            border: 2px solid {BURTS_RED};
            border-radius: 14px;
            width: calc(33% - 20px);
            padding: 16px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
            cursor: pointer;
            transition: transform 0.15s ease;
        }}

        .trend-card:hover {{
            transform: scale(1.03);
        }}

        .trend-title {{
            font-size: 18px;
            font-weight: bold;
            color: {BURTS_DARK};
            margin-bottom: 8px;
        }}

        .trend-metric {{
            color: {BURTS_DARK};
            font-size: 15px;
            margin-bottom: 4px;
        }}

        .priority-pill {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }}

        .High {{
            background-color: {BURTS_RED};
        }}
        .Medium {{
            background-color: {BURTS_GOLD};
        }}
        .Low {{
            background-color: #ffe88a;
            color: {BURTS_DARK};
        }}

        /* Insight cards */
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
# Header Bar
# ------------------------------------------------------
st.markdown("""
<div class="header-bar">
    <div class="header-title">Burt’s Bees Trend Sensing Dashboard</div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------
# Helper Functions
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


def render_trend_card(trend, growth, priority):
    """Produce a card in HTML."""
    safe = trend.replace(" ", "_")
    return f"""
        /?trend={safe}#deepdive
            <div class="trend-title">🍯 {trend}</div>
            <div class="trend-metric">Growth: {growth}%</div>
            <div class="priority-pill {priority}">{priority}</div>
        </div>
    """


def render_card_grid(df):
    html = '<div class="card-grid">'
    for _, row in df.iterrows():
        html += render_trend_card(row["Trend"], row["Growth %"], row["Priority"])
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
# TAB SETUP
# ------------------------------------------------------
df = generate_mock_trends()

tabs = st.tabs([
    "Quarterly Snapshot",
    "Trend Explorer",
    "Trend Deep Dive"
])


# ------------------------------------------------------
# TAB 1 — Quarterly Snapshot
# ------------------------------------------------------
with tabs[0]:
    st.header("Quarterly Snapshot")

    top_growing = df.sort_values("Growth %", ascending=False).head(5)
    top_declining = df.sort_values("Growth %", ascending=True).head(5)

    st.subheader("Top 5 Fastest Growing Trends")
    render_card_grid(top_growing)

    st.subheader("Top 5 Declining Trends")
    render_card_grid(top_declining)


# ------------------------------------------------------
# TAB 2 — Trend Explorer
# ------------------------------------------------------
with tabs[1]:
    st.header("Explore All Trends")
    render_card_grid(df)


# ------------------------------------------------------
# TAB 3 — Trend Deep Dive
# ------------------------------------------------------
with tabs[2]:
    st.markdown('<a name="deepdive"></a>', unsafe_allow_html=True)
    st.header("Trend Deep Dive")

    trend_param = st.query_params.get("trend", [None])[0]
    if trend_param:
        st.session_state.selected_trend = trend_param.replace("_", " ")

    selected = st.session_state.selected_trend or df["Trend"].iloc[0]

    st.subheader(f"Selected Trend: {selected}")

    render_insight_card(
        "Why This Trend Matters",
        f"'{selected}' continues to rise as consumers prioritize effective, natural ingredients."
    )

    render_insight_card(
        "Consumer Need",
        f"'{selected}' connects to core needs: hydration, simplicity, and skin-first wellness."
    )

    render_insight_card(
        "Opportunity for Burt’s Bees",
        f"Leverage '{selected}' in future innovations, limited editions, and ingredient-forward storytelling."
    )

    st.subheader("Simulated Trend Trajectory")
    st.line_chart(np.random.randint(50, 100, size=12))
