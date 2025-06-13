# 💰 Revenue Rescue  
**Predict Future Business Revenue with AI-Powered Insights**

**Revenue Rescue** is an AI-driven platform that helps businesses forecast future revenue, understand key influencing factors like customer churn or seasonal drops, and receive intelligent business suggestions through an integrated AI chatbot. Built for simplicity, clarity, and power, the tool enables data-driven decision-making using machine learning and explainable AI.

---

## 🚀 Features

- 📈 Revenue prediction with ML models (XGBoost, Stacking)
- 🧠 SHAP-based insights to explain revenue drivers
- 🤖 AI chatbot for business strategy recommendations
- 📊 Interactive visualizations for trends and performance
- 📑 Automated, human-readable business reports
- 🖥️ Streamlit UI with clean HTML/CSS styling

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Frontend:** Streamlit, HTML, CSS  
- **Data Processing:** Pandas, NumPy  
- **ML Models:** Scikit-learn, XGBoost  
- **Explainability:** SHAP  
- **Visualization:** Matplotlib, Seaborn  
- **AI Chatbot:** Deepseek API

---

## 🧠 Workflow

1. Load historical revenue & business metric data  
2. Preprocess and engineer features  
3. Train ML models and evaluate (R², MAE, RMSE)  
4. Predict revenue and visualize results  
5. Explain predictions with SHAP  
6. Chat with the AI assistant for actionable insights

---

## 📊 Use Cases

- Sales forecasting for business planning  
- Financial performance monitoring  
- Growth and marketing strategy optimization  
- AI-driven business advisory (via chatbot)

---

## 📁 Data Requirements

- Historical revenue data  
- Date/time column (monthly, quarterly, etc.)  
- Business KPIs (e.g., ad spend, user count)

---

## ▶️ How to Run

```bash
git clone https://github.com/yourusername/revenue-rescue.git
cd revenue-rescue
pip install -r requirements.txt
streamlit run streamlit-connection.py
