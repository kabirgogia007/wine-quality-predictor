
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# 1. Configuration & Styling
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="VinoVeritas | Premium Wine Quality Estimator",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Theme Colors
PRIMARY_COLOR = "#800020"  # Burgundy
SECONDARY_COLOR = "#FFD700"  # Gold
BACKGROUND_COLOR = "#1E1E1E" # Dark Gray
TEXT_COLOR = "#F5F5F5"

# Custom CSS for that "Classy Wine" feel
st.markdown(f"""
<style>
    .stApp {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
    }}
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border-radius: 8px;
        border: 1px solid {SECONDARY_COLOR};
        font-weight: bold;
    }}
    div[data-testid="stSidebar"] {{
        background-color: #2b2b2b;
        border-right: 1px solid {SECONDARY_COLOR};
    }}
    h1, h2, h3 {{
        color: {SECONDARY_COLOR} !important;
        font-family: 'Playfair Display', serif;
    }}
    .wine-card {{
        background-color: #2b2b2b;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid {PRIMARY_COLOR};
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. Load Resources
# ------------------------------------------------------------------------------
@st.cache_resource
def load_resources():
    try:
        model = joblib.load("best_model_wine_quality.joblib")
        with open("feature_names.json", "r") as f:
            features = json.load(f)
        with open("metrics.json", "r") as f:
            metrics = json.load(f)
        return model, features, metrics
    except FileNotFoundError:
        return None, None, None

model, feature_names, metrics = load_resources()

# ------------------------------------------------------------------------------
# 3. Sidebar Inputs
# ------------------------------------------------------------------------------
st.sidebar.title("🍷 Wine Characteristics")
st.sidebar.markdown("Adjust the physicochemical properties below.")

input_data = {}

if feature_names:
    for feature in feature_names:
        # Define reasonable ranges (based on typical wine data)
        # We could dynamicall load these min/max if we saved them, but hardcoding
        # defaults or using broad ranges is safe for a demo.
        if "acidity" in feature:
            min_val, max_val, default = 0.0, 15.0, 7.0
        elif "sugar" in feature:
             min_val, max_val, default = 0.0, 50.0, 5.0
        elif "alcohol" in feature:
             min_val, max_val, default = 8.0, 15.0, 10.0
        elif "pH" in feature:
            min_val, max_val, default = 2.0, 4.5, 3.2
        else:
             min_val, max_val, default = 0.0, 100.0, 10.0
        
        input_data[feature] = st.sidebar.slider(
            feature.replace('_', ' ').title(), 
            min_value=float(min_val), 
            max_value=float(max_val), 
            value=float(default)
        )

# ------------------------------------------------------------------------------
# 4. Main Interface
# ------------------------------------------------------------------------------
st.title("VinoVeritas 🍷")
st.markdown("### *The Art & Science of Wine Quality Prediction*")
st.markdown("---")

if model is None:
    st.error("⚠️ Model files not found! Please run `train_model.py` first.")
    st.info("The backend needs to generate the model and metadata artifacts.")
else:
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔮 Prediction", "📊 Data Insights", "ℹ️ Model Info"])

    with tab1:
        st.subheader("Sommelier's Assessment")
        
        # Predict Button
        if st.button("Evaluate Quality", use_container_width=True):
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]
            
            # Advisor Logic
            score = round(prediction, 1)
            if score >= 7.5:
                verdict = "Exceptional Vintage"
                desc = "This wine shows outstanding complexity and balance. A truly superior choice suitable for aging."
                color = "#FFD700"  # Gold
            elif score >= 6.0:
                verdict = "Fine Table Wine"
                desc = "A solid, enjoyable wine with good character. Perfect for daily consumption or casual dining."
                color = "#C0C0C0"  # Silver
            else:
                verdict = "Below Average"
                desc = "This wine may have noticeable flaws or lacks balance. Might be best used for cooking or sangria."
                color = "#cd7f32" # Bronze

            # Display Result
            st.markdown(f"""
            <div class="wine-card">
                <h2 style="color: {color}; margin-bottom: 0;">{score} / 10</h2>
                <h4 style="margin-top: 5px;">{verdict}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Feature Breakdown (Mock attribution or simple display)
            with st.expander("See Input Summary"):
                st.dataframe(input_df)

    with tab2:
        st.subheader("Exploratory Analysis")
        st.markdown("Visualizations of the training dataset.")
        
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists("eda_histograms.png"):
                st.image("eda_histograms.png", caption="Feature Distributions", use_container_width=True)
            else:
                st.warning("Histograms not found.")
        
        with col2:
            if os.path.exists("eda_correlation.png"):
                st.image("eda_correlation.png", caption="Feature Correlations", use_container_width=True)
            else:
                st.warning("Correlation Matrix not found.")
        
        if os.path.exists("eda_quality_dist.png"):
            st.image("eda_quality_dist.png", caption="Quality Score Distribution", use_container_width=True)

    with tab3:
        st.subheader("Model Performance")
        st.markdown("Current model metrics calculated on the test set.")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("R² Score", f"{metrics['r2']:.3f}")
        m_col2.metric("RMSE", f"{metrics['rmse']:.3f}")
        m_col3.metric("MAE", f"{metrics['mae']:.3f}")
        
        st.markdown("---")
        st.json(feature_names, expanded=False)

