import streamlit as st
import joblib
import pandas as pd

# Load saved model
model = joblib.load('saved_models/rf_model.pkl')

# App layout
st.title('Titanic Survival Predictor')
st.sidebar.header('Passenger Details')

# Input widgets
def user_input():
    pclass = st.sidebar.selectbox('Class', [1, 2, 3])
    sex = st.sidebar.selectbox('Sex', ['male', 'female'])
    age = st.sidebar.slider('Age', 0, 100, 30)
    sibsp = st.sidebar.slider('Siblings/Spouses', 0, 8, 0)
    parch = st.sidebar.slider('Parents/Children', 0, 6, 0)
    fare = st.sidebar.slider('Fare (£)', 0, 200, 50)
    embarked = st.sidebar.selectbox('Embarked', ['S', 'C', 'Q'])
    
    return {
        'Pclass': pclass,
        'Sex': 0 if sex == 'male' else 1,
        'Age': age,
        'SibSp': sibsp,
        'Parch': parch,
        'Fare': fare,
        'Embarked': embarked
    }

# Prediction function
def predict_survival(data):
    df = pd.DataFrame(data, index=[0])
    prediction = model.predict(df)
    probability = model.predict_proba(df)
    return prediction[0], probability[0][1]

# Main app
user_data = user_input()

if st.sidebar.button('Predict Survival'):
    pred, proba = predict_survival(user_data)
    st.subheader('Prediction Result')
    result = 'Survived' if pred == 1 else 'Did Not Survive'
    st.write(f'Prediction: {result}')
    st.write(f'Probability of Survival: {proba:.2%}')
    st.balloons()