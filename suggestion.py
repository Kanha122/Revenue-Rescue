import streamlit as st
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

def generate_suggestions():
    api_key = os.getenv("TOGETHER_API_KEY")
    client = Together()

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[
            {
                "role": "user",
                "content":"Act as a business innovation expert. Generate 5 completely new, creative, and practical business growth strategies that can help a company reduce financial losses, increase profitability, and attract new customers. Each strategy should be concise (1–3 sentences), actionable, and distinct from commonly repeated advice. Do not number or bullet the suggestions—just return each as a standalone sentence, separated by a line break. Ensure every request gives different, unique ideas."
            }
        ]
    )
    return response.choices[0].message.content

st.set_page_config(page_title="Revenue Rescue Ideas", layout="wide")
st.title("💡 Business Suggestions")

st.markdown("Click the button below to generate powerful business ideas to reduce losses and boost customer attraction.")

if st.button("🚀 Generate Suggestions"):
    with st.spinner("Thinking..."):
        suggestions_text = generate_suggestions()
    st.session_state.suggestions = [s.strip() for s in suggestions_text.split("\n") if s.strip()]

if st.session_state.suggestions:
    for idx, suggestion in enumerate(st.session_state.suggestions, 1):
        st.markdown(
            f"""
            <div style="background-color:#f9fbfc;padding:15px;margin-bottom:12px;border-radius:10px;
                        border-left: 4px solid #3498db; box-shadow: 1px 1px 6px rgba(0,0,0,0.05);">
                <h4 style="margin:0 0 5px 0; font-size:16px; color:#1a5276;">Suggestion #{idx}</h4>
                <p style="margin:0; font-size:15px; color:#2c3e50;">{suggestion}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("🧹 Clear All Suggestions"):
            st.session_state.suggestions = []
            st.rerun()
            

