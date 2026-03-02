import streamlit as st
import pandas as pd
import numpy as np
import random
import os

# ------------------------------------------------
# OPENAI CLIENT SETUP (KEY COMMENTED OUT)
# ------------------------------------------------

# from openai import OpenAI
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

openai_client = None  # dashboard runs without key


# ------------------------------------------------
# AI GENERATION FUNCTION (SAFE WITHOUT KEY)
# ------------------------------------------------

def ai_generate(prompt: str):
    """
    Returns placeholder text if OPENAI_API_KEY is not set.
    Otherwise would call OpenAI for real trend insights.
    """
    if openai_client is None:
        return "(AI output disabled — add OPENAI_API_KEY to enable real insights.)"

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a senior beauty trend analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"OpenAI Error: {e}"


# ------------------------------------------------
# MOCK TREND DATA
# ------------------------------------------------

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


# ------------------------------------------------
# STREAMLIT UI
# ------------------------------------------------

st.set_page_config(page_title="Burt’s Bees Trend Sensing Prototype", layout="wide")

st.title("Burt’s Bees Trend Sensing Tool Prototype")
st.caption("AI disabled for now — dashboard loads with simulated data.")

tabs = st.tabs([
    "Quarterly Snapshot", 
    "Trend Explorer", 
    "Trend Deep Dive", 
    "Source Simulation", 
    "Recommendations"
])


# ------------------------------------------------
# TAB 1 — QUARTER SNAPSHOT
# ------------------------------------------------

with tabs[0]:
    st.header("Quarterly Snapshot")
    df = generate_mock_trends()

    col1, col2, col3 = st.columns(3)
    col1.metric("High Priority", len(df[df["Priority"] == "High"]))
    col2.metric("Medium Priority", len(df[df["Priority"] == "Medium"]))
    col3.metric("Low Priority", len(df[df["Priority"] == "Low"]))

    st.dataframe(df, use_container_width=True)


# ------------------------------------------------
# TAB 2 — TREND EXPLORER
# ------------------------------------------------

with tabs[1]:
    st.header("Explore Trends")
    search = st.text_input("Search trends, ingredients, claims…")
    filtered = df[df["Trend"].str.contains(search, case=False)] if search else df
    st.dataframe(filtered, use_container_width=True)


# ------------------------------------------------
# TAB 3 — TREND DEEP DIVE
# ------------------------------------------------

with tabs[2]:
    st.header("Trend Deep Dive")
    trend = st.selectbox("Select a trend", df["Trend"])

    st.subheader("AI-Generated Insight (Disabled)")
    insight_prompt = f"""
    Explain why the trend '{trend}' is emerging in beauty, what consumer need it aligns with,
    and how Burt’s Bees could respond.
    """

    if st.button("Generate Insight"):
        st.write(ai_generate(insight_prompt))

    st.subheader("Simulated Trend Trajectory")
    st.line_chart(simulate_time_series())


# ------------------------------------------------
# TAB 4 — SOURCE SIMULATION
# ------------------------------------------------

with tabs[3]:
    st.header("Simulated External Data Signals")

    source = st.selectbox("Choose a source", [
        "Spate (Search Trends)",
        "Lux Motivebase (Conversation Themes)",
        "Mintel (Claims & Innovation)",
        "Meltwater (Social Buzz)"
    ])

    if st.button("Generate Source Simulation"):
        st.write("(AI simulation disabled — add key to activate.)")


# ------------------------------------------------
# TAB 5 — RECOMMENDATIONS
# ------------------------------------------------

with tabs[4]:
    st.header("AI-Generated Innovation Recommendations")

    prompt = """
    Provide 5 innovation opportunities based on emerging beauty trends.
    """

    if st.button("Generate Recommendations"):
        st.write(ai_generate(prompt))

