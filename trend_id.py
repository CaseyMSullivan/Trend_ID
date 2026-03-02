import streamlit as st
import pandas as pd
import numpy as np
import random

# ---------------------------------------
# BRAND STYLING (Burt’s Bees Colors)
# ---------------------------------------

BURTS_RED = "#E41D22"
BURTS_YELLOW = "#F9CC46"
BURTS_GOLD = "#DCA426"
BURTS_DARK = "#4A2C2A"
BURTS_OFFWHITE = "#FFF8E7"

# ---------------------------------------
# CUSTOM STREAMLIT CSS
# ---------------------------------------

st.markdown(f"""
    <style>
        .main {{
            background-color: {BURTS_OFFWHITE};
        }}
        .reportview-container {{
            background-color: {BURTS_OFFWHITE};
        }}
        h1, h2, h3, h4 {{
            color: {BURTS_DARK} !important;
        }}
        .stMetric {{
            background-color: {BURTS_YELLOW}20;
            padding: 10px;
            border-radius: 8px;
        }}
        .block-container {{
            padding-top: 2rem;
        }}
        .header-bar {{
            background-color: {BURTS_RED};
            padding: 18px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .header-title {{
            color: white;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
        }}
    </style>
""", unsafe_allow_html=True)


# ---------------------------------------
# OPTIONAL: Add logo
# ---------------------------------------

# If you have a logo file (burt_logo.png), put it in your folder and uncomment:
# st.image("burt_logo.png", width=180)


# ---------------------------------------
# Branded Header Bar
# ---------------------------------------

st.markdown("""
<div class="header-bar">
    <div class="header-title">Burt’s Bees Trend Sensing Dashboard</div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------
# MOCK DATA (unchanged)
# ---------------------------------------

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


# ---------------------------------------
# STREAMLIT UI
# ---------------------------------------

tabs = st.tabs([
    "Quarterly Snapshot",
    "Trend Explorer",
    "Trend Deep Dive",
    "Source Simulation",
    "Recommendations"
])

# ---------------------------------------
# TAB 1 — Quarterly Snapshot
# ---------------------------------------

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


# ---------------------------------------
# TAB 2 — Trend Explorer
# ---------------------------------------

with tabs[1]:
    st.header("Explore Trends")
    search = st.text_input("Search trends, ingredients, claims…")

    filtered = df[df["Trend"].str.contains(search, case=False)] if search else df

    st.dataframe(filtered, use_container_width=True)


# ---------------------------------------
# TAB 3 — Trend Deep Dive
# ---------------------------------------

with tabs[2]:
    st.header("Trend Deep Dive")

    trend = st.selectbox("Select a trend", df["Trend"])

    st.subheader("Insight (AI‑powered analysis disabled during prototype)")
    st.info("Connect OpenAI API key to enable insights.")

    st.subheader("Simulated Trend Trajectory")
    st.line_chart(simulate_time_series())


# ---------------------------------------
# TAB 4 — Source Simulation
# ---------------------------------------

with tabs[3]:
    st.header("Simulated External Signals")

    source = st.selectbox("Choose a source", [
        "Spate (Search Trends)",
        "Lux Motivebase (Conversation Themes)",
        "Mintel (Claims & Innovation)",
        "Meltwater (Social Buzz)"
    ])

    if st.button("Generate Simulation"):
        st.success("AI output disabled — add OpenAI key to activate.")


# ---------------------------------------
# TAB 5 — Recommendations
# ---------------------------------------

with tabs[4]:
    st.header("Recommendations (AI‑powered when activated)")

    if st.button("Generate Innovation Recommendations"):
        st.warning("AI disabled — enable OpenAI API key for recommendations.")

