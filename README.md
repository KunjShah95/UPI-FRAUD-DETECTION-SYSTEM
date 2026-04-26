# 🚨 UPI Fraud Detection System

![Repo Size](https://img.shields.io/github/repo-size/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM)
![Contributors](https://img.shields.io/github/contributors/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM)
![Stars](https://img.shields.io/github/stars/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM?style=social)
![Forks](https://img.shields.io/github/forks/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM?style=social)

A modern Streamlit-based machine learning app for detecting potentially fraudulent UPI transactions in both **single** and **batch** modes.

---

## ✨ What’s inside

- **Single Transaction Prediction** with validation and fraud probability display.
- **Batch CSV Prediction** with downloadable prediction output.
- **Risk Insights Dashboard** with rich analytics charts.
- **Top Navbar Navigation** (Overview, Single, Batch, Risk Insights, Recent Activity).
- **Dark/Light Theme Toggle** in sidebar.
- **Export Buttons** for risk insights summary and high-risk transactions.
- **Model Performance Panel** in sidebar (Accuracy, F1, ROC-AUC).

---

## 🧱 Tech Stack

- Python
- Streamlit
- scikit-learn
- Plotly
- Pandas / NumPy

---

## 📁 Current project structure

```text
UPI-FRAUD-DETECTION-SYSTEM/
├── main.py
├── requirements.txt
├── UPI Fraud Detection updated.pkl
├── DEPLOYMENT.md
├── Data_Analysis_for_UPI_Payment_System.ipynb
├── Copy of Sample_DATA.csv
└── README.md
```

> Note: `main.py` at the repository root is the active app entrypoint.

---

## 🚀 Quick Start (Local)

### 1) Clone and install

```bash
git clone https://github.com/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM.git
cd UPI-FRAUD-DETECTION-SYSTEM
pip install -r requirements.txt
```

### 2) Run the app

```bash
streamlit run main.py
```

### 3) Use the app

- Go to **Single Prediction** for instant checks.
- Go to **Batch Analytics** to upload CSV and generate predictions.
- Go to **Risk Insights** for advanced visual analysis.

---

## 📊 Visual Analytics available

Depending on available columns in your uploaded CSV, the app renders charts such as:

- Fraud vs Legit distribution
- Amount distribution by prediction
- Fraud probability distribution
- Prediction by payment gateway
- Risk band distribution
- Transaction type breakdown
- Amount vs frequency scatter
- Age distribution by prediction

The app includes fallback logic for column naming differences (e.g., `location`, `city`, `region`).

---

## 🧠 Model & Pipeline

- Training/analysis notebook: `Data_Analysis_for_UPI_Payment_System.ipynb`
- Saved artifact: `UPI Fraud Detection updated.pkl`
  - Contains model, scaler, feature columns, and optional metrics
- Dependency pin:
  - `scikit-learn==1.6.1` (required for artifact compatibility)

---

## 🗂️ Input expectations

- **Single Prediction:** Use app form fields.
- **Batch Prediction:** Upload CSV with transaction fields compatible with training schema.

If some columns are missing, the app still attempts prediction by aligning encoded features with the model’s required columns.

---

## ☁️ Deployment

See [`DEPLOYMENT.md`](./DEPLOYMENT.md) for complete platform-wise instructions:

- Streamlit Community Cloud
- Render
- Railway
- Azure App Service

It also includes a dedicated section on handling the `.pkl` file safely in production.

---

## ✅ Pre-run checklist

- `requirements.txt` installed
- `UPI Fraud Detection updated.pkl` present in root
- `main.py` runs without syntax errors

Quick smoke test:

```bash
python -m py_compile main.py
streamlit run main.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## 📬 Support

For issues/suggestions, open a GitHub issue in this repository.

---

## 🪪 License

MIT License