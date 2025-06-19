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