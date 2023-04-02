import streamlit as st
import pandas as pd
import pickle

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

# Define the feature names
features = ['InternetService_1', 'InternetService_2', 'Contract_1', 'Contract_2', 
            'SeniorCitizen_1', 'No Internet Service_1', 'TechSupport_Yes', 
            'OnlineSecurity_Yes', 'Dependents_Yes','tenure', 'MonthlyCharges', 'TotalCharges']

# Define a mapping of options to their corresponding numeric values
options_mapping = {
    'InternetService_1': {'No': 0, 'DSL': 1, 'Fiber optic': 2},
    'InternetService_2': {'No': 0, 'DSL': 1, 'Fiber optic': 2},
    'Contract_1': {'Month-to-month': 0, 'One year': 1, 'Two year': 2},
    'Contract_2': {'Month-to-month': 0, 'One year': 1, 'Two year': 2},
    'SeniorCitizen_1': {'No': 0, 'Yes': 1},
    'No Internet Service_1': {'No': 0, 'Yes': 1},
    'TechSupport_Yes': {'No': 0, 'Yes': 1},
    'OnlineSecurity_Yes': {'No': 0, 'Yes': 1},
    'Dependents_Yes': {'No': 0, 'Yes': 1}
}

# Define a function to get user input
def get_user_input():
    inputs = {}
    for feature in features:
        if feature in ['tenure', 'MonthlyCharges', 'TotalCharges']:
            inputs[feature] = st.sidebar.number_input(feature)
        else:
            options_mapping = {
                'InternetService_1': {0: 'No', 1: 'DSL'},
                'InternetService_2': {0: 'No', 1: 'Fiber optic'},
                'Contract_1': {0: 'Month-to-month', 1: 'One year', 2: 'Two year'},
                'Contract_2': {0: 'No', 1: 'Yes'},
                'SeniorCitizen_1': {0: 'No', 1: 'Yes'},
                'No Internet Service_1': {0: 'No', 1: 'Yes'},
                'TechSupport_Yes': {0: 'No', 1: 'Yes'},
                'OnlineSecurity_Yes': {0: 'No', 1: 'Yes'},
                'Dependents_Yes': {0: 'No', 1: 'Yes'}
            }
            options = list(options_mapping[feature].keys())
            options_labels = list(options_mapping[feature].values())
            inputs[feature] = options[options_labels.index(st.sidebar.selectbox(feature, options_labels))]
    return inputs

# Define a function to make a prediction
def predict_churn(inputs):
    df = pd.DataFrame([inputs])
    prediction = model.predict_proba(df)[:,1][0]
    return prediction

# Define the app layout
def app():
    st.title('Customer Churn Prediction App')
    st.sidebar.header('Input Features')
    inputs = get_user_input()
    st.write('Selected Features:')
    st.write(inputs)
    churn_probability = predict_churn(inputs)
    if churn_probability >= 0.5:
        st.write('Based on the selected features, the customer is likely to churn.')
    else:
        st.write('Based on the selected features, the customer is not likely to churn.')

# Run the app
if __name__ == '__main__':
    app()