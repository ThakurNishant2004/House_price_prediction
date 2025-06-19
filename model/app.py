import streamlit as st
import numpy as np
import pickle
import pandas as pd
from PIL import Image
from pathlib import Path
import io

# ✅ This must come first — before any other st command
# App Configuration
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# # Now you can use other Streamlit commands
# st.title("House Price Prediction App")

# Load model, scaler, and column names
@st.cache_resource
def load_artifacts():
    base_path = Path(__file__).parent
    with open(base_path / "model.pkl", "rb") as f:
        model = pickle.load(f)
    with open(base_path / "scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open(base_path / "columns.pkl", "rb") as f:
        columns = pickle.load(f)
    return model, scaler, columns
model, scaler, columns = load_artifacts()



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

    
# Additional features in expandable section
with st.expander("Additional Features", expanded=False):
    st.subheader("Amenities & Other Features")
    col3, col4 = st.columns(2)
    
    with col3:
        furnishing = st.radio("Furnishing Status", 
                            ("Unfurnished", "Semi-Furnished", "Furnished"),
                            horizontal=True)
        parking = st.checkbox("Parking Available")
        
    with col4:
        preferred_area = st.checkbox("Preferred Location")
        main_road = st.checkbox("Facing Main Road")

# Prepare input data
input_data = {
    'area': area,
    'price_per_sq_feet_area': price_per_sqft,
    'total_rooms': bedrooms + bathrooms,  # Assuming total_rooms includes both
    'age': age,
    'furnishingstatus_furnished': 1 if furnishing == "Furnished" else 0,
    'furnishingstatus_semi-furnished': 1 if furnishing == "Semi-Furnished" else 0,
    'furnishingstatus_unfurnished': 1 if furnishing == "Unfurnished" else 0,
    'prefarea_yes': 1 if preferred_area else 0,
    # Add other binary features based on your model requirements
}

# Ensure all columns are present (fill missing with 0)
for col in columns:
    if col not in input_data:
        input_data[col] = 0

# Convert to DataFrame and scale
input_df = pd.DataFrame([input_data])[columns]  # Ensure correct column order
input_scaled = scaler.transform(input_df)

# Prediction button with better layout
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
with col_btn2:
    predict_btn = st.button("Predict House Price", use_container_width=True)

# Display results
if predict_btn:
    with st.spinner('Calculating estimated price...'):
        prediction = model.predict(input_scaled)[0]
        
        # Format the price with commas and add currency symbol
        formatted_price = f"₹ {int(prediction):,}"
        
        # Display with nice styling
        st.markdown(f"""
        <div style='text-align: center; margin-top: 20px;'>
            <h3 style='color: #2c3e50;'>Estimated House Price:</h3>
            <div style='font-size: 32px; color: #4CAF50; font-weight: bold;'>
                {formatted_price}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional info based on price
        st.markdown("---")
        if prediction > 5000000:
            st.info("💎 This is a premium property. Consider comparing with similar listings in the area.")
        elif prediction > 2000000:
            st.info("🏡 This is a mid-range property. Good value for the features offered.")
        else:
            st.info("📈 This is an affordable property. Potential for good returns on investment.")

# Add footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>Note: This prediction is an estimate based on the provided features.</p>
        <p>For accurate valuation, consult with a real estate professional.</p>
    </div>
""", unsafe_allow_html=True)