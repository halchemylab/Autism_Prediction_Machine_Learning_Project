import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Load the trained model
try:
    svc_model = joblib.load('svc_model.pkl')
except FileNotFoundError:
    st.error("Error: svc_model.pkl not found. Please make sure it's in the same directory as this app.")
    st.stop()

# AQ Questions
aq_questions = {
    'A1': 'I prefer to do things the same way over and over again.',
    'A2': 'I often notice small sounds when others do not.',
    'A3': 'I usually concentrate more on the whole picture than small details.',
    'A4': 'I find it hard to make new friends.',
    'A5': 'I notice patterns in things all the time.',
    'A6': 'I find social situations easy.',
    'A7': 'I tend to notice details that others don’t.',
    'A8': 'I find it difficult to imagine what characters are thinking or feeling.',
    'A9': 'I prefer to go to a library than a party.',
    'A10': 'I find it hard to understand jokes and sarcasm.'
}

# --- Streamlit App ---
st.title("✅ Autism :rainbow[Spectrum] Screening Tool")
st.markdown("Please answer the following questions honestly.")

with st.form("autism_screening_form"):
    st.subheader("Autism Quotient (AQ) Questions")
    answers = {}
    for key, question in aq_questions.items():
        answers[key] = st.radio(question, options=['Yes', 'No'], index=1) # Default to No

    st.subheader("Additional Information")
    age = st.number_input("Age", min_value=0, step=1)
    gender = st.selectbox("Gender", options=['Male', 'Female', 'Other'])
    ethnicity = st.selectbox("Ethnicity", options=['Asian', 'Black', 'Hispanic', 'Native American', 'White', 'Other'])

    submitted = st.form_submit_button("Submit")

    if submitted:
        # Process AQ answers
        aq_score = sum(1 for answer in answers.values() if answer == 'Yes')

        # Prepare input data for the model
        user_data = {
            'A1': 1 if answers['A1'] == 'Yes' else 0,
            'A2': 1 if answers['A2'] == 'Yes' else 0,
            'A3': 1 if answers['A3'] == 'Yes' else 0,
            'A4': 1 if answers['A4'] == 'Yes' else 0,
            'A5': 1 if answers['A5'] == 'Yes' else 0,
            'A6': 0 if answers['A6'] == 'Yes' else 1, # Reverse for A6
            'A7': 1 if answers['A7'] == 'Yes' else 0,
            'A8': 1 if answers['A8'] == 'Yes' else 0,
            'A9': 1 if answers['A9'] == 'Yes' else 0,
            'A10': 1 if answers['A10'] == 'Yes' else 0,
            'age': age,
            'gender': gender,
            'ethnicity': ethnicity
        }
        user_df = pd.DataFrame([user_data])

        # Encode categorical features (assuming your model was trained with encoded features)
        label_encoders = {}
        for column in ['gender', 'ethnicity']:
            le = LabelEncoder()
            user_df[column] = le.fit_transform(user_df[column])
            label_encoders[column] = le # Store for potential future use

        # Make prediction
        prediction = svc_model.predict(user_df)

        st.subheader("Prediction Result")
        if prediction[0] == 1:
            st.warning("Based on your responses, the screening suggests a higher likelihood of autism spectrum traits.")
        else:
            st.success("Based on your responses, the screening suggests a lower likelihood of autism spectrum traits.")

        # Optional: Display probability/confidence (if the model has a predict_proba method)
        if hasattr(svc_model, "predict_proba"):
            probability = svc_model.predict_proba(user_df)[0][1] * 100
            st.info(f"Probability of autism spectrum traits: {probability:.2f}%")

        # Optional: Show bar chart of AQ score
        st.subheader("Your Autism Quotient (AQ) Score")
        st.write(f"Your score: {aq_score} out of 10")
        chart_data = pd.DataFrame({'Score': [aq_score], 'Max': [10]})
        st.bar_chart(chart_data[['Score', 'Max']])

st.markdown("---")
st.info("""
This tool is not a diagnosis. For a professional evaluation, please consult a licensed clinician. 
You can find more information and resources at the Autism Society website: [https://www.autism-society.org/](https://www.autism-society.org/) 
""")