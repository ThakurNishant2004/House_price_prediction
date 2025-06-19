import streamlit as st
import numpy as np
import pickle
import pandas as pd
from PIL import Image
from pathlib import Path
import io

# Load model, scaler, and column names
@st.cache_resource
def load_artifacts():
    model = pickle.load(open("model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    columns = pickle.load(open("columns.pkl", "rb"))
    return model, scaler, columns

model, scaler, columns = load_artifacts()

# App Configuration
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stNumberInput, .stSelectbox {
        background-color: white;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success {
        font-size: 20px !important;
        color: #28a745 !important;
    }
    .header {
        color: #2c3e50;
    }
    .uploaded-image {
        max-width: 100%;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)