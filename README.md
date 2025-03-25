# 🌈 Autism Spectrum Disorder Prediction Project

A machine learning application that predicts the likelihood of autism spectrum disorder (ASD) based on behavioral and personal characteristics.

## 📚 Project Overview

This project implements a screening tool for autism spectrum disorder using machine learning. It includes:
- Data analysis and visualization of autism spectrum characteristics
- Multiple machine learning models for prediction
- A Streamlit web application for easy interaction with the model

## 🔧 Technologies Used

- Python 3.x
- Libraries:
  - Streamlit (Web Application)
  - Scikit-learn (Machine Learning)
  - Pandas (Data Processing)
  - Matplotlib/Seaborn (Visualization)
  - Joblib (Model Serialization)

## 📊 Model Performance

The project evaluated multiple machine learning models:

| Model           | Accuracy | Precision | Recall | F1 Score |
|----------------|----------|-----------|--------|----------|
| SVC (Selected) | 83.2%    | 68.4%     | 78.8%  | 73.2%    |
| Logistic Reg.  | 83.2%    | 69.4%     | 75.8%  | 72.5%    |
| KNN            | 80.5%    | 64.9%     | 72.7%  | 68.6%    |
| Random Forest  | 79.6%    | 66.7%     | 60.6%  | 63.5%    |
| Decision Tree  | 73.5%    | 54.3%     | 57.6%  | 55.9%    |

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/autism_prediction_machine_learning_project.git
cd autism_prediction_machine_learning_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

## 📱 Using the Application

1. Fill out the questionnaire with:
   - 10 behavioral questions (AQ-10 screening)
   - Personal information (age, gender, ethnicity)
2. Submit the form
3. View the prediction results, including:
   - Likelihood of ASD traits
   - Probability score
   - AQ-10 score interpretation

## ⚠️ Disclaimer

This tool is designed for screening purposes only and should not be used as a diagnostic tool. Please consult healthcare professionals for proper medical diagnosis.

## 📁 Project Structure

```
autism_prediction_machine_learning_project/
├── README.md           # Project documentation
├── analysis.ipynb      # Data analysis and model development
├── app.py             # Streamlit web application
├── svc_model.pkl      # Trained SVC model
└── dataset.csv        # Original dataset
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](your-repo-url/issues).

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Henry Pai (halchemylabs)

## 🙏 Acknowledgments

- Dataset source: 
  - UCI Machine Learning Repository
  - [Kaggle Autism Diagnosis Competition](https://www.kaggle.com/competitions/autismdiagnosis)
- Autism Society of America for resources and information