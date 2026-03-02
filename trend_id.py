import streamlit as st
import pandas as pd
import numpy as np
import random

# ------------------------------------------------------
# BURT'S BEES BRAND COLORS (from uploaded logo image)
# ------------------------------------------------------
BURTS_YELLOW = "#F4C32D"
BURTS_RED = "#C51F25"
BURTS_DARK = "#4A2C2A"
BURTS_OFFWHITE = "#FFF8E7"
BURTS_GOLD = "#DFAF2B"

# ------------------------------------------------------
# STREAMLIT BASE STYLING
# ------------------------------------------------------
st.set_page_config(page_title="Burt’s Bees Trend Sensing Dashboard", layout="wide")

st.markdown(f"""
    <style>
        .main {{
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

        h1, h2, h3, h4 {{
            color: {BURTS_DARK} !important;
        }}

        .stMetric {{
            background-color: {BURTS_YELLOW}50;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid {BURTS_RED}20;
        }}

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
# OPTIONAL: BURT'S BEES LOGO
# ------------------------------------------------------
# Place the logo in the same folder as app.py and uncomment this:
# st.image("burtsbees_logo.png", width=160)

# ------------------------------------------------------
# Header Bar
# ------------------------------------------------------
st.markdown("""
<div class="header-bar">
    <div class="header-title">Burt’s Bees Trend Sensing Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# HELPER FUNCTIONS
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
            "Growth %": round(random.uniform(5, 60), 2),
            "QoQ Change": random.choice(["Increasing", "Stable", "Declining"])
        })
    return pd.DataFrame(rows)

def simulate_time_series():
    base = np.random.randint(40, 100)
    return [base + random.randint(-8, 12) for _ in range(12)]

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
# BUILD TABS
# ------------------------------------------------------
tabs = st.tabs([
    "Quarterly Snapshot",
    "Trend Explorer",
    "Trend Deep Dive",
    "Source Simulation",
    "Recommendations"
])

# ------------------------------------------------------
# TAB 1 — QUARTERLY SNAPSHOT
# ------------------------------------------------------
with tabs[0]:
    st.header("Quarterly Snapshot")

    df = generate_mock_trends()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("High Priority", len(df[df["Priority"] == "High"]))
    with col2:
        st.metric("Medium Priority", len(df[df["Priority"] == "Medium"]))
    with col3:
        st.metric("Low Priority", len(df[df["Priority"] == "Low"]))

    st.write("")
    st.dataframe(df, use_container_width=True)

# ------------------------------------------------------
# TAB 2 — TREND EXPLORER
# ------------------------------------------------------
with tabs[1]:
    st.header("Explore Trends")
    search = st.text_input("Search trends, ingredients, claims…")

    filtered = df[df["Trend"].str.contains(search, case=False)] if search else df

    st.dataframe(filtered, use_container_width=True)

# ------------------------------------------------------
# TAB 3 — TREND DEEP DIVE (with Visual Insight Cards)
# ------------------------------------------------------
with tabs[2]:
    st.header("Trend Deep Dive")

    trend = st.selectbox("Select a trend", df["Trend"])

    st.subheader("Visual Insights")

    render_insight_card(
        title="Why This Trend Matters",
        body=f"""
        The '{trend}' trend reflects a shift toward natural, gentle, 
        and functional ingredients. Beauty consumers are increasingly 
        searching for solutions aligned with simplicity and performance.
        """
    )

    render_insight_card(
        title="Consumer Need",
        body=f"""
        Consumers prioritize hydration, barrier support, and multi-benefit 
        care. '{trend}' connects strongly to holistic skin and lip wellness.
        """
    )

    render_insight_card(
        title="Opportunity for Burt’s Bees",
        body=f"""
        This trend aligns with Burt’s Bees' nature-powered heritage. 
        Opportunities include ingredient-forward storytelling, 
        limited editions, and category extensions.
        """
    )

    st.subheader("Simulated Trend Trajectory")
    st.line_chart(simulate_time_series())

# ------------------------------------------------------
# TAB 4 — SOURCE SIMULATION
# ------------------------------------------------------
with tabs[3]:
    st.header("Simulated External Signals")

    source = st.selectbox("Choose a source", [
        "Spate (Search Trends)",
        "Lux Motivebase (Conversation Themes)",
        "Mintel (Claims & Innovation)",
        "Meltwater (Social Buzz)"
    ])

    if st.button("Generate Simulation"):
        st.success("AI output disabled — connect OpenAI API to activate.")

# ------------------------------------------------------
# TAB 5 — RECOMMENDATIONS
# ------------------------------------------------------
with tabs[4]:
    st.header("Recommendations")

    if st.button("Generate Innovation Recommendations"):
        st.warning("AI disabled — enable OpenAI API key for insights.")
