import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import mutual_info_classif
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, StackingClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_curve, roc_auc_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE
from itertools import combinations
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import shap
import streamlit as st
import warnings

def generate_pdf_report(classification_rep, auc, churn_loss, interventions, total_loss, profit_saved,
                        pie_chart_path, roc_curve_path, shap_plot_path, top_10_features, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Page 1: Business impact, pie chart, classification report, ROC curve
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Revenue Rescue Analytics Report")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, height - 100, "📊 Business Impact Summary:")

    y = height - 120
    c.setFont("Helvetica", 12)
    metrics = [
        ("Churn Loss", churn_loss),
        ("Intervention Cost", interventions),
        ("Total Loss", total_loss),
        ("Profit Saved", profit_saved)
    ]
    for label, value in metrics:
        c.drawString(60, y, f"{label}: ${value:,.2f}")
        y -= 15

    # Classification report
    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, y - 20, "📋 Classification Report:")
    y -= 40
    c.setFont("Helvetica", 9)
    for line in classification_rep.strip().split('\n'):
        c.drawString(60, y, line)
        y -= 12

    # AUC Score
    y -= 20
    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, y, f"🔍 ROC-AUC Score: {auc:.4f}")
    y -= 30

    # Pie Chart
    if os.path.exists(pie_chart_path):
        c.drawImage(pie_chart_path, 50, y - 180, width=250, height=180)

    # ROC Curve
    if os.path.exists(roc_curve_path):
        c.drawImage(roc_curve_path, 310, y - 180, width=250, height=180)

    # End of Page 1
    c.showPage()

    # Page 2: SHAP Analysis
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "🧠 Model Explainability: SHAP Analysis")

    y = height - 80
    if os.path.exists(shap_plot_path):
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "📌 SHAP Feature Importance Plot:")
        y -= 20
        c.drawImage(shap_plot_path, 50, y - 250, width=500, height=280)
        y -= 270

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Top 10 Most Influential Features:")
    y -= 25
    c.setFont("Helvetica", 10)
    for feature, val in top_10_features:
        c.drawString(60, y, f"{feature}: {val:.4f}")
        y -= 15
    
    c.showPage()

    c.save()

def run_churn_pipeline(df, target_column="Churn", revenue_per_customer=1000, cost_per_intervention=200):
    warnings.filterwarnings("ignore")

    # 1. Load and preprocess data
    df = df.drop(columns=[col for col in ['customerID', 'CustomerID', 'ID'] if col in df.columns], errors='ignore')
    df = df.apply(pd.to_numeric, errors='ignore')
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.fillna(df.select_dtypes(include=np.number).median(), inplace=True)
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    le = LabelEncoder()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # 2. Feature Engineering
    if all(col in df.columns for col in ['MonthlyCharges', 'tenure']):
        X['MonthlyCharges_to_Tenure'] = df['MonthlyCharges'] / (df['tenure'] + 1)
    if all(col in df.columns for col in ['TotalCharges', 'tenure']):
        X['TotalCharges_to_Tenure'] = df['TotalCharges'] / (df['tenure'] + 1)
    if 'tenure' in df.columns:
        X['Tenure_Bucket'] = pd.cut(df['tenure'], bins=[0, 12, 24, 48, 72, 100], labels=[1, 2, 3, 4, 5])
        X['Tenure_Bucket'] = le.fit_transform(X['Tenure_Bucket'].astype(str))

    interaction_features = {}
    for col1, col2 in combinations(X.columns, 2):
        if np.issubdtype(X[col1].dtype, np.number) and np.issubdtype(X[col2].dtype, np.number):
            interaction_features[f"{col1}_{col2}"] = X[col1] * X[col2]
    X_interactions = pd.DataFrame(interaction_features)
    X = pd.concat([X, X_interactions], axis=1)

    kmeans = KMeans(n_clusters=5, random_state=42)
    df['CustomerSegment'] = kmeans.fit_predict(X)

    iso = IsolationForest(contamination=0.05, random_state=42)
    df['Anomaly'] = iso.fit_predict(X)

    mi_scores = mutual_info_classif(X.fillna(0), y)
    selected_features = X.columns[np.argsort(mi_scores)[-20:]]
    X = X[selected_features]

    smote = SMOTE(random_state=42)
    X, y = smote.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 4. Train models
    base_models = [
        ('xgb', XGBClassifier()),
        ('lgbm', LGBMClassifier()),
        ('catboost', CatBoostClassifier(verbose=0)),
        ('rf', RandomForestClassifier())
    ]
    stacking = StackingClassifier(estimators=base_models, final_estimator=RandomForestClassifier())
    models = {
        "LogisticRegression": LogisticRegression(),
        "XGBoost": XGBClassifier(),
        "LightGBM": LGBMClassifier(),
        "CatBoost": CatBoostClassifier(verbose=0),
        "RandomForest": RandomForestClassifier(),
        "StackingClassifier": stacking
    }

    results = {}
    roc_curves = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
        results[name] = {"Accuracy": acc, "ROC_AUC": roc_auc}
        fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
        roc_curves[name] = (fpr, tpr)

    # 5. Select best model
    best_model_name = max(results, key=lambda x: results[x]["ROC_AUC"])
    best_model = models[best_model_name]
    best_preds = best_model.predict(X_test)
    best_proba = best_model.predict_proba(X_test)[:, 1]

   # 6. Business Impact
    false_neg = np.sum((y_test == 1) & (best_preds == 0))
    churn_loss = false_neg * revenue_per_customer
    interventions = np.sum(best_preds == 1) * cost_per_intervention
    total_loss = churn_loss + interventions
    total_revenue = len(y_test) * revenue_per_customer
    profit_saved = total_revenue - total_loss
    
    # Ensure no negative values
    churn_loss = max(0, churn_loss)
    interventions = max(0, interventions)
    total_loss = abs(total_loss)
    profit_saved = max(0, profit_saved)
    
    # Log the values to help debug
    print(f"Total revenue: ${total_revenue:.2f}")
    print(f"Churn Loss: ${churn_loss:.2f}")
    print(f"Intervention Cost: ${interventions:.2f}")
    print(f"Total Loss: ${total_loss:.2f}")
    print(f"Profit Saved: ${profit_saved:.2f}")
    
    # Save Pie Chart
    labels = ["Churn Loss", "Intervention Cost", "Total Loss", "Profit Saved"]
    sizes = [churn_loss, interventions, total_loss, profit_saved]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    explode = (0.1, 0.1, 0.1, 0)
    pie_chart_path = "pie_chart.png"
    
    # Check if any values are negative or NaN before plotting
    if any(np.isnan(x) or x < 0 for x in sizes):
        st.error("Error: Negative or NaN values detected in business metrics.")
    else:
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, 
                autopct='%1.1f%%', startangle=140, shadow=True)
        plt.title(f"📊 Business Impact Analysis")
        plt.axis('equal')
        plt.savefig(pie_chart_path)
        plt.close()
    

    # Save ROC Curve
    fpr, tpr = roc_curves[best_model_name]
    auc = roc_auc_score(y_test, best_proba)
    roc_curve_path = "roc_curve.png"
    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, color='blue', label=f"{best_model_name} AUC = {auc:.2f}")
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curve - {best_model_name}")
    plt.legend()
    plt.grid(True)
    plt.savefig(roc_curve_path)
    plt.close()
    

     # Fallback for SHAP explanation
    if isinstance(best_model, StackingClassifier):
        print("⚠️ SHAP does not support StackingClassifier. Falling back to best individual model.")
        individual_models = {k: v for k, v in models.items() if k != "StackingClassifier"}
        best_model_name = max(individual_models, key=lambda x: results[x]["ROC_AUC"])
        best_model = individual_models[best_model_name]
        best_model.fit(X_train, y_train)
        best_preds = best_model.predict(X_test)
        best_proba = best_model.predict_proba(X_test)[:, 1]

    shap.initjs()
    explainer = shap.Explainer(best_model, X_test)
    shap_values = explainer(X_test)
    shap_plot_path = "shap_summary_plot.png"
    plt.figure()
    shap.summary_plot(shap_values, X_test, show=False)
    plt.tight_layout()
    plt.savefig(shap_plot_path, bbox_inches='tight')
    plt.close()

    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    feature_importance = sorted(zip(X.columns, mean_abs_shap), key=lambda x: x[1], reverse=True)
    top_10_features = feature_importance[:10]

    # Generate PDF
    classification_rep = classification_report(y_test, best_preds)
    generate_pdf_report(
        classification_rep,
        auc,
        churn_loss,
        interventions,
        total_loss,
        profit_saved,
        pie_chart_path,
        roc_curve_path,
        shap_plot_path,
        top_10_features,
        output_path="churn_report.pdf"
    )
    st.success(f"\n✅ Report saved as: churn_report.pdf")
