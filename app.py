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
            'A1_Score': 1 if answers['A1'] == 'Yes' else 0,
            'A2_Score': 1 if answers['A2'] == 'Yes' else 0,
            'A3_Score': 1 if answers['A3'] == 'Yes' else 0,
            'A4_Score': 1 if answers['A4'] == 'Yes' else 0,
            'A5_Score': 1 if answers['A5'] == 'Yes' else 0,
            'A6_Score': 0 if answers['A6'] == 'Yes' else 1,  # Reverse for A6
            'A7_Score': 1 if answers['A7'] == 'Yes' else 0,
            'A8_Score': 1 if answers['A8'] == 'Yes' else 0,
            'A9_Score': 1 if answers['A9'] == 'Yes' else 0,
            'A10_Score': 1 if answers['A10'] == 'Yes' else 0,
            'age': age,
            'gender_f': 1 if gender == 'Female' else 0,
            'gender_m': 1 if gender == 'Male' else 0,
            'gender_o': 1 if gender == 'Other' else 0,
            'result': aq_score,  # Total AQ score
            'jaundice_no': 0,  # Default values for jaundice
            'jaundice_yes': 0,
            'used_app_before_no': 1  # Default value for app usage
        }
        user_df = pd.DataFrame([user_data])

        # Make prediction
        prediction = svc_model.predict(user_df)

        # Enhanced Prediction Result Section
        st.markdown("<h2 style='text-align: center;'>🔍 Screening Results</h2>", unsafe_allow_html=True)
        
        # Create three columns for the main result
        left_col, center_col, right_col = st.columns([1, 2, 1])
        
        # Calculate probability if available
        probability = 0
        if hasattr(svc_model, "predict_proba"):
            probability = svc_model.predict_proba(user_df)[0][1] * 100

        # Display main prediction result in a colored box
        with center_col:
            if prediction[0] == 1:
                st.markdown("""
                    <div style='background-color: rgba(255, 190, 190, 0.3); padding: 20px; border-radius: 10px; text-align: center;'>
                        <h3 style='color: #ff4b4b;'>Higher Likelihood</h3>
                        <p>of autism spectrum traits detected</p>
                        <h1 style='font-size: 48px;'>🔔</h1>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background-color: rgba(190, 255, 190, 0.3); padding: 20px; border-radius: 10px; text-align: center;'>
                        <h3 style='color: #00cc00;'>Lower Likelihood</h3>
                        <p>of autism spectrum traits detected</p>
                        <h1 style='font-size: 48px;'>✓</h1>
                    </div>
                """, unsafe_allow_html=True)

        # Show probability gauge if available
        if hasattr(svc_model, "predict_proba"):
            st.markdown("<br>", unsafe_allow_html=True)
            prob_cols = st.columns([1, 3, 1])
            with prob_cols[1]:
                st.markdown(f"""
                    <div style='background-color: rgba(230, 230, 230, 0.3); padding: 20px; border-radius: 10px; text-align: center;'>
                        <h4>Probability Indicator</h4>
                        <div style='margin: 10px 0;'>
                            <div style='background-color: #e6e6e6; border-radius: 10px; height: 20px;'>
                                <div style='background-color: {"#ff4b4b" if probability > 50 else "#00cc00"}; 
                                          width: {probability}%; height: 100%; border-radius: 10px;'></div>
                            </div>
                        </div>
                        <p style='font-size: 24px; margin: 10px;'>{probability:.1f}%</p>
                    </div>
                """, unsafe_allow_html=True)

        # Display AQ Score in an enhanced format
        st.markdown("<br>", unsafe_allow_html=True)
        score_cols = st.columns([1, 2, 1])
        with score_cols[1]:
            st.markdown(f"""
                <div style='background-color: rgba(230, 230, 230, 0.3); padding: 20px; border-radius: 10px; text-align: center;'>
                    <h4>Autism Quotient (AQ) Score</h4>
                    <h2 style='font-size: 36px; margin: 10px;'>{aq_score}/10</h2>
                    <div style='background-color: #e6e6e6; border-radius: 10px; height: 20px;'>
                        <div style='background-color: #3366ff; width: {(aq_score/10)*100}%; height: 100%; border-radius: 10px;'></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Add score interpretation guide
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background-color: rgba(230, 230, 230, 0.2); padding: 15px; border-radius: 10px;'>
                <h4 style='text-align: center;'>Score Interpretation Guide</h4>
                <ul style='list-style-type: none;'>
                    <li>🟢 0-3: Lower likelihood of autism traits</li>
                    <li>🟡 4-6: Moderate presence of autism traits</li>
                    <li>🔴 7-10: Higher likelihood of autism traits</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")
st.info("""
This tool is not a diagnosis. For a professional evaluation, please consult a licensed clinician. 
You can find more information and resources at the Autism Society website: [https://www.autism-society.org/](https://www.autism-society.org/) 
""")