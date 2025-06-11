import streamlit as st
from streamlit_extras.let_it_rain import rain

st.set_page_config(
    page_title="Home | Churn Prediction",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
    <style>
        .info-card h2 {
            color: #00C49A;
            font-weight: bold;
            box-shadow: 0 0 15px rgba(0, 196, 154, 0.2);
        }

        .info-highlight {
            background-color: #00C49A;
            color: black;
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: bold;
        }

        .fun-fact {
            background-color: #0B1B2B;
            border-left: 5px solid #00C49A;
            padding: 10px 20px;
            margin-top: 30px;
            border-radius: 10px;
            font-style: italic;
            color: #cce7e0;
        }

        .custom-circle-img {
            width: 400px;
            height: 400px;
            object-fit: cover;
            border-radius: 50%;
            margin-left: 25%;
            margin-top: 5%;
            border: 6px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 8px 24px rgba(255, 255, 255, 0.2), 0 0 30px rgba(0, 196, 154, 0.3);
            transition: all 0.3s ease-in-out;
        }

        .custom-circle-img:hover {
            transform: scale(1.05);
            box-shadow: 0 12px 32px rgba(255, 255, 255, 0.3), 0 0 40px rgba(0, 196, 154, 0.5);
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Revenue Rescue</h1>", unsafe_allow_html=True)


left, right = st.columns(2)


with left:
    st.markdown("<h2>🧠 Know Your Customers</h2>", unsafe_allow_html=True)
    st.markdown("""
        Predicting customer churn isn't just about numbers — it's about understanding **why customers leave** and **what you can do to stop them**.

        With our AI-powered Platform, you can:
        - 🔍 Identify high-risk customers
        - 💬 Understand behaviors through insights
        - 🎯 Launch targeted retention strategies
        - 📈 Boost lifetime value & ROI

        <div class='fun-fact'>
            🤔 <strong>Did you know?</strong><br>
            It costs <span class='info-highlight'>$5–10x more</span> to acquire a new customer than to keep an existing one.
        </div>
    """, unsafe_allow_html=True)

with right:
        st.markdown(
            f'<img class="custom-circle-img" src="data:image/jpeg;base64,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"/>',
            unsafe_allow_html=True
        )
rain(
    emoji="💰",
    font_size=40,
    falling_speed=5,
    animation_length="infinite"
)
if st.button("Generate Revenue Analysis"):
    st.switch_page("churn-generator.py")

st.markdown("---")
st.markdown("© 2025 Revenue Rescue. All rights reserved.")