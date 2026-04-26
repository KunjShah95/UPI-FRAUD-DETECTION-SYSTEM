import os
import pickle

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title='UPI Fraud Detection System', page_icon='🔍', layout='wide')

st.markdown(
    """
    <style>
        .block-container {padding-top: 1.2rem; padding-bottom: 1.2rem;}
        .hero-card {
            background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 45%, #0EA5E9 100%);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 16px;
            color: #F8FAFC;
        }
        .small-caption {color: #94A3B8; font-size: 0.9rem;}
        div[data-testid="stHorizontalBlock"] div[role="radiogroup"] {
            background: #0f172a;
            padding: 0.4rem;
            border-radius: 12px;
            border: 1px solid #1e293b;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def find_column(df: pd.DataFrame, candidates: list[str]):
    lower_map = {c.lower(): c for c in df.columns}
    for cand in candidates:
        found = lower_map.get(cand.lower())
        if found:
            return found
    return None


# Load model bundle
BASE_DIR = os.path.dirname(__file__)
MODEL_FILENAME = 'UPI Fraud Detection updated.pkl'
MODEL_CANDIDATES = [
    os.path.join(BASE_DIR, MODEL_FILENAME),
    os.path.join(BASE_DIR, '..', MODEL_FILENAME),
]
MODEL_PATH = next((p for p in MODEL_CANDIDATES if os.path.exists(p)), None)

if MODEL_PATH is None:
    st.error('Model file not found. Expected one of: ' + ', '.join(os.path.abspath(p) for p in MODEL_CANDIDATES))
    st.stop()

with open(MODEL_PATH, 'rb') as f:
    loaded_obj = pickle.load(f)

if not isinstance(loaded_obj, dict):
    st.error('Model file does not contain full pipeline. Please retrain and save with scaler and feature_columns.')
    st.stop()

model = loaded_obj['model']
scaler = loaded_obj['scaler']
feature_columns = loaded_obj['feature_columns']
metrics = loaded_obj.get('performance_metrics', None)


# Session state
if 'last_batch_df' not in st.session_state:
    st.session_state['last_batch_df'] = None
if 'recent_preds' not in st.session_state:
    st.session_state['recent_preds'] = []


# Sidebar
st.sidebar.title('UPI Fraud Detection System')
st.sidebar.info('Predict fraudulent UPI transactions in real time and via batch analytics.')
st.sidebar.markdown('---')

theme_mode = st.sidebar.radio('Display Mode', ['Dark', 'Light'], horizontal=True)
if theme_mode == 'Light':
    st.markdown(
        """
        <style>
            .stApp { background-color: #F8FAFC; color: #0F172A; }
            .hero-card {
                background: linear-gradient(135deg, #E2E8F0 0%, #CBD5E1 45%, #93C5FD 100%);
                color: #0F172A;
            }
            .small-caption { color: #334155; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
            .stApp { background-color: #0B1220; color: #F8FAFC; }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.markdown('---')
st.sidebar.header('How to use')
st.sidebar.markdown(
    '''
1. Fill single transaction details and click **Predict Transaction**.
2. Upload a CSV for **Batch Prediction + Graphs**.
3. Open **Risk Insights** for deeper patterns.
4. Download enriched results and insights.
'''
)

if metrics:
    st.sidebar.markdown('---')
    st.sidebar.subheader('Model Performance')
    st.sidebar.write(f"**Accuracy:** {metrics.get('Accuracy', 0):.2f}")
    st.sidebar.write(f"**F1-Score:** {metrics.get('F1_Score', 0):.2f}")
    st.sidebar.write(f"**ROC-AUC:** {metrics.get('ROC_AUC', 0):.2f}")

st.sidebar.markdown('---')
st.sidebar.subheader('Live Snapshot')
if st.session_state['last_batch_df'] is not None and not st.session_state['last_batch_df'].empty:
    side_df = st.session_state['last_batch_df']
    pred_col = find_column(side_df, ['Prediction'])
    gateway_col = find_column(side_df, ['Payment_Gateway', 'payment_gateway', 'gateway'])
    prob_col = find_column(side_df, ['Fraud_Probability'])

    total_side = len(side_df)
    fraud_side = int((side_df[pred_col] == 'Fraud').sum()) if pred_col else 0
    st.sidebar.metric('Last Batch Size', f'{total_side:,}')
    st.sidebar.metric('Detected Frauds', f'{fraud_side:,}')
    st.sidebar.metric('Fraud Rate', f'{(fraud_side / total_side * 100) if total_side else 0:.2f}%')

    if prob_col:
        st.sidebar.caption(f"Avg Fraud Probability: {side_df[prob_col].mean():.2%}")

    if pred_col and gateway_col:
        top_gateway = side_df[side_df[pred_col] == 'Fraud'][gateway_col].value_counts().head(1)
        if not top_gateway.empty:
            st.sidebar.caption(f"Top Risk Gateway: {top_gateway.index[0]}")
else:
    st.sidebar.caption('Upload a CSV to unlock live risk KPIs here.')

st.sidebar.markdown('---')
st.sidebar.caption('Tip: Start from **Batch Analytics** for richer Risk Insights charts.')


# Header + nav
st.markdown(
    """
    <div class="hero-card">
        <h2 style="margin:0;">🔍 UPI Fraud Detection Command Center</h2>
        <p style="margin-top:8px;">Analyze single or batch transactions, detect fraud, and explore risk insights with visual analytics.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

nav_choice = st.radio(
    'Navigation',
    ['🏠 Overview', '🧾 Single Prediction', '📊 Batch Analytics', '🚨 Risk Insights', '🕓 Recent Activity'],
    horizontal=True,
    label_visibility='collapsed',
)

errors = []
prediction = None
submitted = False


if nav_choice == '🏠 Overview':
    c1, c2, c3 = st.columns(3)
    c1.info('Use **Single Prediction** for real-time checks.')
    c2.info('Use **Batch Analytics** for CSV uploads and visual charts.')
    c3.info('Use **Risk Insights** to investigate suspicious patterns.')

    st.markdown('### Quick Highlights')
    if st.session_state['last_batch_df'] is not None:
        latest_df = st.session_state['last_batch_df']
        pred_col = find_column(latest_df, ['Prediction'])
        total_txn = len(latest_df)
        fraud_count = int((latest_df[pred_col] == 'Fraud').sum()) if pred_col else 0
        fraud_rate = (fraud_count / total_txn * 100) if total_txn else 0
        h1, h2, h3 = st.columns(3)
        h1.metric('Last Batch Size', f'{total_txn:,}')
        h2.metric('Fraud Count', f'{fraud_count:,}')
        h3.metric('Fraud Rate', f'{fraud_rate:.2f}%')
    else:
        st.warning('No batch data available yet. Upload a CSV in Batch Analytics to unlock insights.')


if nav_choice == '🧾 Single Prediction':
    st.subheader('Single Transaction Prediction')
    col1, col2 = st.columns(2)

    with st.form('single_pred_form'):
        with col1:
            amount = st.number_input('Transaction Amount', min_value=0.0, step=0.01)
            transaction_type = st.selectbox('Transaction Type', ['P2P', 'P2M', 'M2P', 'Other'])
            payment_gateway = st.selectbox('Payment Gateway', ['Paytm', 'PhonePe', 'GooglePay', 'AmazonPay', 'Other'])
            merchant_category = st.selectbox('Merchant Category', ['Retail', 'Food', 'Travel', 'Other'])
        with col2:
            device_os = st.selectbox('Device OS', ['Android', 'iOS', 'Other'])
            transaction_frequency = st.number_input('Transaction Frequency', min_value=0, step=1)
            customer_age = st.number_input('Customer Age', min_value=0, step=1)
            location = st.text_input('Location', placeholder='e.g., Mumbai, Delhi, Bengaluru')

        submitted = st.form_submit_button('Predict Transaction', width='stretch')

    if submitted:
        if amount < 0:
            errors.append('Amount cannot be negative.')
        if not location.strip():
            errors.append('Location is required.')

        if errors:
            for err in errors:
                st.error(err)
        else:
            try:
                input_df = pd.DataFrame(
                    {
                        'amount': [amount],
                        'Transaction_Type': [transaction_type],
                        'Payment_Gateway': [payment_gateway],
                        'Merchant_Category': [merchant_category],
                        'Device_OS': [device_os],
                        'Transaction_Frequency': [transaction_frequency],
                        'customer_age': [customer_age],
                        'location': [location],
                    }
                )
                input_encoded = pd.get_dummies(input_df)
                for col in feature_columns:
                    if col not in input_encoded.columns:
                        input_encoded[col] = 0
                input_encoded = input_encoded[feature_columns]

                input_scaled = scaler.transform(input_encoded)
                prediction = model.predict(input_scaled)[0]

                st.markdown('### Prediction Result')
                r1, r2 = st.columns([1, 2])
                with r1:
                    st.error('🚨 Fraud') if prediction == 1 else st.success('✅ Legit')
                with r2:
                    if prediction == 1:
                        st.markdown(':red[Be cautious! This transaction is likely fraudulent.]')
                    else:
                        st.markdown(':green[This transaction appears safe.]')
                    if hasattr(model, 'predict_proba'):
                        prob = float(model.predict_proba(input_scaled)[0][1])
                        st.progress(min(max(prob, 0.0), 1.0), text=f'Fraud probability: {prob:.2%}')
            except Exception as e:
                st.error(f'Prediction failed: {e}')


if nav_choice == '📊 Batch Analytics':
    st.subheader('Batch Prediction (CSV Upload)')
    uploaded_file = st.file_uploader('Upload CSV file with transactions', type=['csv'])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            drop_cols = ['Transaction_ID', 'Date', 'Time', 'Merchant_ID', 'Customer_ID', 'Device_ID', 'IP_Address']
            df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

            df_encoded = pd.get_dummies(df)
            for col in feature_columns:
                if col not in df_encoded.columns:
                    df_encoded[col] = 0
            df_encoded = df_encoded[feature_columns]

            df_scaled = scaler.transform(df_encoded)
            preds = model.predict(df_scaled)
            df['Prediction'] = ['Fraud' if p == 1 else 'Legit' for p in preds]

            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(df_scaled)
                if proba.shape[1] > 1:
                    df['Fraud_Probability'] = np.round(proba[:, 1], 4)

            st.session_state['last_batch_df'] = df.copy()

            total_txn = len(df)
            fraud_count = int((df['Prediction'] == 'Fraud').sum())
            legit_count = int((df['Prediction'] == 'Legit').sum())
            fraud_rate = (fraud_count / total_txn * 100) if total_txn else 0

            k1, k2, k3, k4 = st.columns(4)
            k1.metric('Total Transactions', f'{total_txn:,}')
            k2.metric('Fraud Cases', f'{fraud_count:,}')
            k3.metric('Legit Cases', f'{legit_count:,}')
            k4.metric('Fraud Rate', f'{fraud_rate:.2f}%')

            st.markdown('### Prediction Results')
            st.dataframe(df, width='stretch')
            st.download_button('Download Results as CSV', df.to_csv(index=False), file_name='predictions.csv', width='stretch')

            st.markdown('### Visual Analytics')
            gc1, gc2 = st.columns(2)

            with gc1:
                dist_df = df['Prediction'].value_counts().reset_index()
                dist_df.columns = ['Prediction', 'Count']
                st.plotly_chart(
                    px.pie(
                        dist_df,
                        names='Prediction',
                        values='Count',
                        title='Fraud vs Legit Distribution',
                        color='Prediction',
                        color_discrete_map={'Fraud': '#EF4444', 'Legit': '#10B981'},
                    ),
                    width='stretch',
                )

                gateway_col = find_column(df, ['Payment_Gateway', 'payment_gateway', 'gateway'])
                if gateway_col:
                    st.plotly_chart(
                        px.histogram(
                            df,
                            x=gateway_col,
                            color='Prediction',
                            barmode='group',
                            title='Prediction by Payment Gateway',
                            color_discrete_map={'Fraud': '#EF4444', 'Legit': '#10B981'},
                        ),
                        width='stretch',
                    )

            with gc2:
                amount_col = find_column(df, ['amount', 'transaction_amount'])
                if amount_col:
                    st.plotly_chart(
                        px.histogram(
                            df,
                            x=amount_col,
                            color='Prediction',
                            nbins=35,
                            title='Amount Distribution by Prediction',
                            color_discrete_map={'Fraud': '#EF4444', 'Legit': '#10B981'},
                        ),
                        width='stretch',
                    )

                prob_col = find_column(df, ['Fraud_Probability'])
                if prob_col:
                    st.plotly_chart(
                        px.histogram(
                            df,
                            x=prob_col,
                            nbins=30,
                            title='Fraud Probability Distribution',
                            color='Prediction',
                            color_discrete_map={'Fraud': '#EF4444', 'Legit': '#10B981'},
                        ),
                        width='stretch',
                    )

            numeric_candidates = [find_column(df, ['amount']), find_column(df, ['Transaction_Frequency']), find_column(df, ['customer_age']), find_column(df, ['Fraud_Probability'])]
            numeric_cols = [c for c in numeric_candidates if c is not None]
            if len(numeric_cols) >= 2:
                corr = df[numeric_cols].corr(numeric_only=True).round(2)
                st.plotly_chart(px.imshow(corr, text_auto=True, title='Numeric Feature Correlation Heatmap', aspect='auto'), width='stretch')

        except Exception as e:
            st.error(f'Batch prediction failed: {e}')


if nav_choice == '🚨 Risk Insights':
    st.subheader('Risk Insights Dashboard')
    insights_df = st.session_state['last_batch_df']

    if insights_df is None or insights_df.empty:
        st.info('No batch prediction data available yet. Please upload a CSV in Batch Analytics first.')
    else:
        work_df = insights_df.copy()

        location_col = find_column(work_df, ['location', 'city', 'region'])
        gateway_col = find_column(work_df, ['Payment_Gateway', 'payment_gateway', 'gateway'])
        merchant_col = find_column(work_df, ['Merchant_Category', 'merchant_category', 'category'])
        prediction_col = find_column(work_df, ['Prediction'])
        amount_col = find_column(work_df, ['amount', 'transaction_amount'])
        txn_type_col = find_column(work_df, ['Transaction_Type', 'transaction_type', 'type'])
        txn_freq_col = find_column(work_df, ['Transaction_Frequency', 'transaction_frequency', 'frequency'])
        age_col = find_column(work_df, ['customer_age', 'age'])
        fraud_prob_col = find_column(work_df, ['Fraud_Probability'])

        if fraud_prob_col:
            threshold = st.slider('High-risk probability threshold', min_value=0.10, max_value=0.95, value=0.70, step=0.05)
            high_risk_df = work_df[work_df[fraud_prob_col] >= threshold].copy()
            work_df['Risk_Band'] = pd.cut(work_df[fraud_prob_col], bins=[0.0, 0.3, 0.7, 1.0], labels=['Low', 'Medium', 'High'], include_lowest=True)
        else:
            threshold = None
            high_risk_df = work_df[work_df[prediction_col] == 'Fraud'].copy() if prediction_col else work_df.iloc[0:0]

        i1, i2, i3 = st.columns(3)
        i1.metric('Analyzed Transactions', f'{len(work_df):,}')
        i2.metric('High-Risk Transactions', f'{len(high_risk_df):,}')
        i3.metric('High-Risk Share', f'{(len(high_risk_df) / len(work_df) * 100) if len(work_df) else 0:.2f}%')

        left, right = st.columns(2)

        with left:
            # Chart 1: location (or merchant fallback)
            if location_col:
                loc_df = high_risk_df[location_col].value_counts().head(10).rename_axis(location_col).reset_index(name='count')
                if not loc_df.empty:
                    st.plotly_chart(px.bar(loc_df, x=location_col, y='count', title='Top High-Risk Locations'), width='stretch')
            elif merchant_col:
                m_df = high_risk_df[merchant_col].value_counts().head(10).rename_axis(merchant_col).reset_index(name='count')
                if not m_df.empty:
                    st.plotly_chart(px.bar(m_df, x=merchant_col, y='count', title='Top High-Risk Merchant Categories'), width='stretch')

            # Chart 2: amount spread
            if amount_col and prediction_col:
                st.plotly_chart(
                    px.box(
                        work_df,
                        x=prediction_col,
                        y=amount_col,
                        color=prediction_col,
                        title='Transaction Amount Spread by Prediction',
                        color_discrete_map={'Fraud': '#EF4444', 'Legit': '#10B981'},
                    ),
                    width='stretch',
                )

            # Chart 3: scatter
            if amount_col and txn_freq_col and prediction_col:
                st.plotly_chart(
                    px.scatter(
                        work_df,
                        x=txn_freq_col,
                        y=amount_col,
                        color=prediction_col,
                        title='Amount vs Transaction Frequency',
                        opacity=0.65,
                        color_discrete_map={'Fraud': '#EF4444', 'Legit': '#10B981'},
                    ),
                    width='stretch',
                )

        with right:
            # Chart 4: gateways
            if gateway_col:
                pg_df = high_risk_df[gateway_col].value_counts().head(10).rename_axis(gateway_col).reset_index(name='count')
                if not pg_df.empty:
                    st.plotly_chart(px.bar(pg_df, x=gateway_col, y='count', title='Top High-Risk Payment Gateways'), width='stretch')

            # Chart 5: risk bands
            if 'Risk_Band' in work_df.columns:
                rb_df = work_df['Risk_Band'].value_counts().reset_index()
                rb_df.columns = ['Risk_Band', 'Count']
                st.plotly_chart(px.pie(rb_df, names='Risk_Band', values='Count', title='Risk Band Distribution'), width='stretch')

            # Chart 6: transaction type breakdown
            if txn_type_col and prediction_col:
                type_df = work_df.groupby([txn_type_col, prediction_col]).size().reset_index(name='count')
                st.plotly_chart(
                    px.bar(
                        type_df,
                        x=txn_type_col,
                        y='count',
                        color=prediction_col,
                        barmode='group',
                        title='Prediction by Transaction Type',
                        color_discrete_map={'Fraud': '#EF4444', 'Legit': '#10B981'},
                    ),
                    width='stretch',
                )

        st.markdown('### Additional Demographic Insight')
        if age_col and prediction_col:
            st.plotly_chart(
                px.histogram(
                    work_df,
                    x=age_col,
                    color=prediction_col,
                    nbins=30,
                    title='Customer Age Distribution by Prediction',
                    color_discrete_map={'Fraud': '#EF4444', 'Legit': '#10B981'},
                ),
                width='stretch',
            )
        else:
            st.caption('Customer age column not found; include age to unlock this chart.')

        st.markdown('### Most Suspicious Transactions')
        display_cols = [c for c in [amount_col, txn_type_col, gateway_col, merchant_col, location_col, fraud_prob_col, prediction_col] if c]

        if fraud_prob_col and fraud_prob_col in high_risk_df.columns:
            high_risk_df = high_risk_df.sort_values(fraud_prob_col, ascending=False)
        elif amount_col and amount_col in high_risk_df.columns:
            high_risk_df = high_risk_df.sort_values(amount_col, ascending=False)

        if display_cols and not high_risk_df.empty:
            st.dataframe(high_risk_df[display_cols].head(25), width='stretch')
        else:
            msg = f'No transactions crossed risk threshold ({threshold:.2f}).' if threshold is not None else 'No suspicious transactions found in current batch.'
            st.success(msg)

        st.markdown('### Export Insights')
        insights_summary = pd.DataFrame([
            {
                'analyzed_transactions': len(work_df),
                'high_risk_transactions': len(high_risk_df),
                'high_risk_share_pct': round((len(high_risk_df) / len(work_df) * 100) if len(work_df) else 0, 2),
                'risk_threshold': threshold if threshold is not None else 'N/A',
            }
        ])

        ex1, ex2 = st.columns(2)
        with ex1:
            st.download_button(
                'Download Insights Summary (CSV)',
                insights_summary.to_csv(index=False),
                file_name='risk_insights_summary.csv',
                key='download_insights_summary',
                width='stretch',
            )
        with ex2:
            export_df = high_risk_df[display_cols] if display_cols and not high_risk_df.empty else pd.DataFrame()
            st.download_button(
                'Download High-Risk Transactions (CSV)',
                export_df.to_csv(index=False),
                file_name='high_risk_transactions.csv',
                key='download_high_risk',
                width='stretch',
                disabled=export_df.empty,
            )


if submitted and not errors and prediction is not None:
    st.session_state['recent_preds'].append(
        {
            'amount': amount,
            'type': transaction_type,
            'age': customer_age,
            'location': location,
            'result': 'Fraud' if prediction == 1 else 'Legit',
        }
    )


if nav_choice == '🕓 Recent Activity':
    st.subheader('Recent Predictions')
    if st.session_state['recent_preds']:
        recent_df = pd.DataFrame(st.session_state['recent_preds'])
        st.dataframe(recent_df, width='stretch')
        st.plotly_chart(
            px.histogram(
                recent_df,
                x='result',
                title='Recent Prediction Breakdown',
                color='result',
                color_discrete_map={'Fraud': '#EF4444', 'Legit': '#10B981'},
            ),
            width='stretch',
        )
    else:
        st.info('No recent predictions yet. Run a single transaction prediction to populate this section.')


st.markdown("<p class='small-caption'>Built with Streamlit • Interactive fraud insights for UPI transactions</p>", unsafe_allow_html=True)
