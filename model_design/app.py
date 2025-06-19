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
# App Header - Improved Version


# App Header - Optimized Version
header_col1, header_col2 = st.columns([2, 1], gap="small")

with header_col1:
    st.markdown("""
    <div style='padding-bottom: 0.5rem;'>
        <h1 style='margin-bottom: 0.2rem;'>🏠 House Price Prediction</h1>
        <p style='margin-top: 0; color: #555555;'>Enter house features to estimate price in <b>₹</b></p>
    </div>
    """, unsafe_allow_html=True)

with header_col2:
    uploaded_file = st.file_uploader(
        " ",  # Empty label
        type=["png", "jpg", "jpeg"],
        key="house_image_uploader",
        help="Upload house photo"
    )
    
    if uploaded_file:
        st.image(
            Image.open(uploaded_file),
            width=120,  # Optimal preview size
            caption=" "  # Empty caption
        )

col1, col2 = st.columns(2, gap="large")  # Added gap between columns

with col1:
    st.subheader("📏 Property Size & Basics")
    
    # Property Size Section
    st.markdown("**How big is the property?**")
    area = st.slider(
        "Total built area (sq.ft)", 
        300, 15000, 1000, 50,
        help="The total livable area of the house in square feet"
    )
    
    # Divider with better spacing
    st.markdown("<div style='margin: 1.5rem 0;'><hr></div>", unsafe_allow_html=True)
    
    # Location Value Section
    st.markdown("**Location Value**")
    price_per_sqft = st.slider(
        "Area price rate (₹ per sq.ft)", 
        500, 10000, 2000, 100,
        help="Typical price per square foot in this neighborhood"
    )

with col2:
    st.subheader("🛏️ House Characteristics")
    
    # Rooms Section - Improved spacing
    st.markdown("**Rooms**")
    room_cols = st.columns(2)
    
    with room_cols[0]:
        st.markdown("<div style='margin-bottom:-10px; font-weight:bold'>Bedrooms</div>", unsafe_allow_html=True)
        bedrooms = st.selectbox(
            "bedrooms_select", 
            options=range(1, 11), 
            index=2,
            help="Number of dedicated sleeping rooms",
            label_visibility="collapsed"
        )
    
    with room_cols[1]:
        st.markdown("<div style='margin-bottom:-10px; font-weight:bold'>Bathrooms</div>", unsafe_allow_html=True)
        bathrooms = st.selectbox(
            "bathrooms_select", 
            options=range(1, 6), 
            index=1,
            help="Number of full bathrooms",
            label_visibility="collapsed"
        )
    
    # Divider with consistent spacing
    st.markdown("<div style='margin: 1.5rem 0;'><hr></div>", unsafe_allow_html=True)
    
    # Age & Condition Section
    st.markdown("**Property Age & Condition**")
    age = st.slider(
        "Years since construction", 
        0, 50, 5,
        help="How many years ago the house was built"
    )
    
    condition = st.select_slider(
        "Overall condition", 
        options=["Poor", "Fair", "Average", "Good", "Excellent"],
        value="Good",
        help="General state of the property"
    )