import streamlit as st
import time
import pandas as pd
from predictive_analysis import run_churn_pipeline

st.set_page_config(page_title="Churn Generator", page_icon="🔮")
st.markdown("""
    <style>
        .heading {
            font-size: 28px;
            font-weight: bold;
            color: #00C49A;
            text-align: center;
            margin-top: 50px;
        }

        .upload-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 30px;
        }

        .upload-btn {
            margin-top: 20px;
            display: flex;
            justify-content: center;
        }

        .upload-btn button {
            background-color: #00C49A !important;
            color: white !important;
            padding: 15px 40px !important;
            border-radius: 10px !important;
            font-size: 18px !important;
            font-weight: bold;
            border: none;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }

        .upload-btn button:hover {
            background-color: #00A786 !important;
            transform: scale(1.05);
            cursor: pointer;
        }

        .file-uploader {
            margin-top: 30px;
            text-align: center;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)
# ---------------------------------------------------


st.markdown("<div class='heading'>Upload Your Dataset 📈</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(" ", type=["csv"])
st.markdown("NOTE: Make sure that Churn feature is available in the dataset")


if uploaded_file:

    st.markdown("<div class='upload-container'>", unsafe_allow_html=True)
    submit_button = st.button("Predict Revenue Analysis")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit_button:
        success_msg = st.empty()
        success_msg.success(f"File '{uploaded_file.name}' uploaded successfully!")
        time.sleep(2.5)
        success_msg.empty()
        try:
            df = pd.read_csv(uploaded_file)
            if df.empty:
                st.error("The uploaded file is empty!")
            else:
                run_churn_pipeline(df)
        except Exception as e:
            st.error(f"Failed to generate report {e}")

        # PDF download
        try:
            with open("churn_report.pdf", "rb") as f:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=f,
                    file_name="churn_report.pdf",
                    mime="application/pdf"
                )
        except FileNotFoundError:
            st.warning("Report not found. Please make sure the pipeline generates it.")
