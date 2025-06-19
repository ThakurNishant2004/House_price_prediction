# House_price_prediction
This is House prediction website based on ml model , Prediction is based on feature provided may be incorrect , so to known exact amount meet to real state person , this is only for practice purpose 

# 🏠 House Price Prediction Model

This is a machine learning project that predicts house prices based on various features such as number of rooms, area (sq. ft), furnishing status, etc. It includes model training, evaluation, and a web-based frontend built using Streamlit.

## 🚀 Features

- Data preprocessing and feature engineering
- Model training using `scikit-learn`
- Model interpretation using `SHAP` and `LIME`
- Interactive frontend using `Streamlit`

## 📁 Project Structure

├── app.py # Streamlit frontend
├── model.pkl # Trained model
├── scaler.pkl # Scaler used for preprocessing
├── requirements.txt # Python dependencies

## 🧠 ML Model

- **Algorithm**: Linear Regression / Random Forest / XGBoost *(choose yours)*
- **Libraries**: pandas, scikit-learn, SHAP, LIME

## 📊 Input Features (Example)

- `Rooms` — Number of rooms
- `Area (sq. ft)` — Size of the house
- `Furnishing` — 0 = Semi-furnished, 1 = Furnished
- `Location`, etc.

## 🖥️ How to Run Locally

```bash
git clone https://github.com/yourusername/house-price-prediction.git
cd house-price-prediction
pip install -r requirements.txt
streamlit run app.py
