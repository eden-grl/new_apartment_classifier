import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Apartment Rent Classifier", page_icon="🏠")

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    model = joblib.load("rent_classifier_model.pkl")
    return model

model = load_model()

# -----------------------------
# Prescriptive Recommendation
# -----------------------------
def recommend_action(prediction):

    if prediction == 1:
        return {
            "Risk Level": "High Rent",
            "Recommendation": "Verify tenant financial capability before approval",
            "Explanation": "High rental cost may require stronger income stability."
        }

    else:
        return {
            "Risk Level": "Low Rent",
            "Recommendation": "Proceed with normal rental approval process",
            "Explanation": "Lower rental cost presents lower financial risk."
        }

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -----------------------------
# HOME PAGE
# -----------------------------
if st.session_state.page == "home":

    st.title("🏠 Apartment Rent Classification System")

    st.write("""
    This system predicts whether an apartment listing has **Low Rent or High Rent**
    based on its features.
    """)

    if st.button("Start Classification"):
        st.session_state.page = "predict"

# -----------------------------
# PREDICTION PAGE
# -----------------------------
elif st.session_state.page == "predict":

    st.title("Enter Apartment Features")

    bathrooms = st.number_input("Bathrooms", 0, 5, 1)
    bedrooms = st.number_input("Bedrooms", 0, 5, 1)
    square_feet = st.number_input("Square Feet", 200, 5000, 800)

    latitude = st.number_input("Latitude", value=40.0)
    longitude = st.number_input("Longitude", value=-73.0)

    price_type = st.selectbox("Price Type", ["Monthly", "Weekly"])

    has_photo = st.selectbox("Has Photo", ["Yes", "No"])
    pets_allowed = st.selectbox("Pets Allowed", ["Yes", "No"])

    cityname = st.text_input("City Name", "New York")
    state = st.text_input("State", "NY")

    if st.button("Predict Rent Category"):

        input_data = pd.DataFrame({
            "bathrooms":[bathrooms],
            "bedrooms":[bedrooms],
            "square_feet":[square_feet],
            "latitude":[latitude],
            "longitude":[longitude],
            "price_type":[price_type],
            "has_photo":[has_photo],
            "pets_allowed":[pets_allowed],
            "cityname":[cityname],
            "state":[state]
        })

        prediction = model.predict(input_data)[0]
        action = recommend_action(prediction)

        st.subheader("Prediction Result")

        if prediction == 1:
            st.success("💰 High Rent Apartment")
        else:
            st.info("🏡 Low Rent Apartment")

        st.subheader("Risk Level")
        st.write(action["Risk Level"])

        st.subheader("Recommended Action")
        st.write(action["Recommendation"])

        st.subheader("Explanation")
        st.write(action["Explanation"])

    if st.button("Back to Home"):
        st.session_state.page = "home"