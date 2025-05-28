import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
import time

st.set_page_config(page_title="About Us - Revenue Rescue", layout="wide")

# Simulated Animated Headline
placeholder = st.empty()
headlines = [
    "Welcome to Revenue Rescue 🚀",
    "Empowering Your Business with Predictive Insights 📊"
]

for _ in range(2):  # repeat animation twice
    for headline in headlines:
        placeholder.markdown(
            f"<h2 style='text-align: center; color: violet;'>{headline}</h2>",
            unsafe_allow_html=True
        )
        
        time.sleep(1.5)


# Static final heading after animation
placeholder.markdown(
    "<h2 style='text-align: center; color: violet;'>Welcome to Revenue Rescue 🚀</h2>",
    unsafe_allow_html=True
)

colored_header(
    label="About Us",
    description="Where data meets foresight",
    color_name="violet-70"
)

st.write("""
**Revenue Rescue** is a cutting-edge AI-powered tool that predicts your future revenue, helping businesses make proactive, informed decisions.
We combine the power of machine learning, time series forecasting, and data-driven strategy to drive growth and minimize uncertainty.
""")

# Team Section
colored_header("Our Mission", "Turning numbers into opportunities", color_name="blue-30")

st.markdown("""
📌 To **rescue lost revenue** and **unlock hidden opportunities** through accurate predictions  
📌 Empower business leaders to plan ahead with **confidence and clarity**  
📌 Simplify complex data into **actionable insights**
""")

# Features Section
colored_header("What Makes Us Special", "Why choose Revenue Rescue?", color_name="green-70")

cols = st.columns(3)
features = [
    ("📈 Forecast Accuracy", "State-of-the-art models for reliable predictions"),
    ("🧠 Smart Insights", "Beyond numbers — strategy recommendations included"),
    ("🌐 Business-Ready", "Tailored for all industries — retail, SaaS, finance & more")
]

for col, (title, desc) in zip(cols, features):
    with col:
        st.subheader(title)
        st.markdown(desc)

# Visual Appeal
rain(
    emoji="💰",
    font_size=40,
    falling_speed=5,
    animation_length="infinite"
)


# Footer
st.markdown("---")
st.markdown("© 2025 Revenue Rescue. All rights reserved.")
