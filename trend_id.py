import streamlit as st
import pandas as pd
import numpy as np
import random
import os

# -----------------------------
# OPENAI CLIENT SETUP
# -----------------------------
from openai import OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# AI GENERATION FUNCTION
# -----------------------------
def ai_generate(prompt: str):
    """
    Sends a prompt to OpenAI and returns the generated text.
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a senior beauty market analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {e}"


# -----------------------------
# MOCK DATA GENERATION
# -----------------------------
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
    for trend in trends:
        rows.append({
            "Trend": trend,
            "Priority": random.choice(priorities),
            "Growth %": round(random.uniform(5, 60), 2),
            "QoQ Change": random.choice(["Increasing", "Stable", "Declining"])
        })
    return pd.DataFrame(rows)


def simulate_time_series():
    base = np.random.randint(40, 100)
    return [base + random.randint(-8, 12) for _ in range(12)]


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Burt’s Bees Trend Sensing Tool Prototype", layout="wide")

st.title("Burt’s Bees Trend Sensing Tool Prototype")
st.caption("Powered by OpenAI. All data simulated until Spate + Motivebase API integration.")

tabs = st.tabs(["Quarterly Snapshot", "Trend Explorer", "Trend Deep Dive", "Source Simulation", "Recommendations"])


# -----------------------------
# TAB 1 — QUARTER SNAPSHOT
# -----------------------------
with tabs[0]:
    st.header("Quarterly Snapshot")

    df = generate_mock_trends()

    col1, col2, col3 = st.columns(3)
    col1.metric("High Priority", len(df[df["Priority"] == "High"]))
    col2.metric("Medium Priority", len(df[df["Priority"] == "Medium"]))
    col3.metric("Low Priority", len(df[df["Priority"] == "Low"]))

    st.dataframe(df, use_container_width=True)


# -----------------------------
# TAB 2 — TREND EXPLORER
# -----------------------------
with tabs[1]:
    st.header("Explore Trends")

    search = st.text_input("Search trends, ingredients, formats…")

    filtered = df[df["Trend"].str.contains(search, case=False)] if search else df

    st.dataframe(filtered, use_container_width=True)


# -----------------------------
# TAB 3 — TREND DEEP DIVE
# -----------------------------
with tabs[2]:
    st.header("Trend Deep Dive")

    trend = st.selectbox("Select a trend", df["Trend"])

    st.subheader("AI-Generated Market Insight")
    insight_prompt = f"""
    Provide a concise 5-sentence insight about why the trend '{trend}' 
    is emerging in beauty, what consumer needs it aligns with, 
    and how Burt’s Bees should respond from an innovation standpoint.
    """

    if st.button("Generate Insight"):
        st.write(ai_generate(insight_prompt))

    st.subheader("Simulated Trend Trajectory")
    st.line_chart(simulate_time_series())


# -----------------------------
# TAB 4 — SOURCE SIMULATION
# -----------------------------
with tabs[3]:
    st.header("Simulated External Source Signals")

    source = st.selectbox("Choose a source", [
        "Spate (Search Trends)",
        "Lux Motivebase (Conversation Themes)",
        "Mintel (Claims & Innovation)",
        "Meltwater (Social Buzz)"
    ])

    if st.button("Generate Source Simulation"):
        if source == "Spate (Search Trends)":
            prompt = """
            Simulate Spate-like beauty search data.
            Provide 6 search terms, each with a % growth and 1-sentence explanation.
            """
            st.write(ai_generate(prompt))

        elif source == "Lux Motivebase (Conversation Themes)":
            prompt = """
            Simulate consumer conversation clusters for beauty.
            Provide 5 clusters with descriptive themes and associated consumer motivations.
            """
            st.write(ai_generate(prompt))

        elif source == "Mintel (Claims & Innovation)":
            prompt = """
            Simulate Mintel-style claims data.
            Provide a list of trending product claims in natural skincare and lip care.
            """
            st.write(ai_generate(prompt))

        elif source == "Meltwater (Social Buzz)":
            prompt = """
            Simulate social media buzz signals in beauty.
            Provide buzz themes and 6 relevant hashtags.
            """
            st.write(ai_generate(prompt))


# -----------------------------
# TAB 5 — RECOMMENDATIONS
# -----------------------------
with tabs[4]:
    st.header("AI-Generated Recommendations for Burt’s Bees")

    prompt = """
    Provide 5 innovation opportunities Burt’s Bees should explore 
    based on macro beauty trends, consumer behavior shifts, and ingredient momentum.
    """

    if st.button("Generate Innovation Recommendations"):
        st.write(ai_generate(prompt))
