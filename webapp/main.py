import streamlit as st
import pandas as pd
import pickle
import os
import numpy as np

# Sidebar
st.sidebar.title('UPI Fraud Detection System')
st.sidebar.info('Enter transaction details or upload a CSV to predict fraud.')
st.sidebar.markdown('---')
st.sidebar.header('How to use:')
st.sidebar.markdown('''
- Fill in all fields for a single transaction and click **Predict**.
- For batch prediction, upload a CSV with the same columns as used in training.
- Download results after batch prediction.
''')

# Load the trained model, scaler, and feature columns
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'UPI Fraud Detection updated.pkl')
with open(MODEL_PATH, 'rb') as f:
    loaded_obj = pickle.load(f)
    if isinstance(loaded_obj, dict):
        model = loaded_obj['model']
        scaler = loaded_obj['scaler']
        feature_columns = loaded_obj['feature_columns']
        metrics = loaded_obj.get('performance_metrics', None)
    else:
        st.error('Model file does not contain full pipeline. Please retrain and save with scaler and feature_columns.')
        st.stop()

# Show model metrics if available
if metrics:
    st.sidebar.markdown('---')
    st.sidebar.subheader('Model Performance')
    st.sidebar.write(f"**Accuracy:** {metrics.get('Accuracy', 0):.2f}")
    st.sidebar.write(f"**F1-Score:** {metrics.get('F1_Score', 0):.2f}")
    st.sidebar.write(f"**ROC-AUC:** {metrics.get('ROC_AUC', 0):.2f}")

st.title('🔍 UPI Fraud Detection System')
st.write('Predict whether a UPI transaction is fraudulent or legitimate. Fill in the details below or upload a CSV file for batch prediction.')

# --- Single Prediction Form ---
st.header('Single Transaction Prediction')
with st.form('single_pred_form'):
    amount = st.number_input('Transaction Amount', min_value=0.0, step=0.01, help='Enter the amount of the transaction (must be non-negative).')
    transaction_type = st.selectbox('Transaction Type', ['P2P', 'P2M', 'M2P', 'Other'], help='Type of UPI transaction.')
    payment_gateway = st.selectbox('Payment Gateway', ['Paytm', 'PhonePe', 'GooglePay', 'AmazonPay', 'Other'], help='Platform used for payment.')
    merchant_category = st.selectbox('Merchant Category', ['Retail', 'Food', 'Travel', 'Other'], help='Category of the merchant.')
    device_os = st.selectbox('Device OS', ['Android', 'iOS', 'Other'], help='Operating system of the device used.')
    transaction_frequency = st.number_input('Transaction Frequency', min_value=0, step=1, help='Number of transactions by the user in a given period.')
    customer_age = st.number_input('Customer Age', min_value=0, step=1, help='Age of the customer.')
    location = st.text_input('Location', help='Location of the transaction (city, region, etc.).')
    submitted = st.form_submit_button('Predict')

if submitted:
    # Input validation
    errors = []
    if amount < 0:
        errors.append('Amount cannot be negative.')
    if not location.strip():
        errors.append('Location is required.')
    if errors:
        for err in errors:
            st.error(err)
    else:
        try:
            input_dict = {
                'amount': [amount],
                'Transaction_Type': [transaction_type],
                'Payment_Gateway': [payment_gateway],
                'Merchant_Category': [merchant_category],
                'Device_OS': [device_os],
                'Transaction_Frequency': [transaction_frequency],
                'customer_age': [customer_age],
                'location': [location],
            }
            input_df = pd.DataFrame(input_dict)
            # One-hot encode categorical columns
            input_encoded = pd.get_dummies(input_df)
            # Align columns to match training
            for col in feature_columns:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0
            input_encoded = input_encoded[feature_columns]
            # Scale
            input_scaled = scaler.transform(input_encoded)
            # Predict
            prediction = model.predict(input_scaled)[0]
            st.subheader('Prediction Result')
            if prediction == 1:
                st.error('🚨 Fraudulent Transaction Detected!')
                st.markdown(':red[Be cautious! This transaction is likely fraudulent.]')
            else:
                st.success('✅ Transaction is Legitimate.')
                st.markdown(':green[This transaction appears safe.]')
        except Exception as e:
            st.error(f"Prediction failed: {e}")

# --- Batch Prediction (CSV Upload) ---
st.header('Batch Prediction (CSV Upload)')
uploaded_file = st.file_uploader('Upload CSV file with transactions', type=['csv'])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        # Drop unnecessary columns if present
        drop_cols = ['Transaction_ID', 'Date', 'Time', 'Merchant_ID', 'Customer_ID', 'Device_ID', 'IP_Address']
        df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')
        missing_cols = [col for col in feature_columns if col not in df.columns and not any(df.columns.str.startswith(col.split('_')[0]))]
        if missing_cols:
            st.warning(f"The following required columns are missing or not properly formatted: {missing_cols}")
        # One-hot encode
        df_encoded = pd.get_dummies(df)
        for col in feature_columns:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[feature_columns]
        # Scale
        df_scaled = scaler.transform(df_encoded)
        preds = model.predict(df_scaled)
        df['Prediction'] = ['Fraud' if p == 1 else 'Legit' for p in preds]
        st.write('### Results')
        st.dataframe(df)
        st.download_button('Download Results as CSV', df.to_csv(index=False), file_name='predictions.csv')
    except Exception as e:
        st.error(f"Batch prediction failed: {e}")

# --- Recent Predictions Section (Session State) ---
if 'recent_preds' not in st.session_state:
    st.session_state['recent_preds'] = []
if submitted and not errors:
    st.session_state['recent_preds'].append({'amount': amount, 'type': transaction_type, 'age': customer_age, 'location': location, 'result': 'Fraud' if prediction == 1 else 'Legit'})

if st.session_state['recent_preds']:
    st.header('Recent Predictions')
    st.table(pd.DataFrame(st.session_state['recent_preds']))

