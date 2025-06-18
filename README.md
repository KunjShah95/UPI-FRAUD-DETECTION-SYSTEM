# 🚨 UPI Fraud Detection System

![UPI Fraud Detection Banner](https://img.shields.io/github/repo-size/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM)
![Contributors](https://img.shields.io/github/contributors/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM)
![Stars](https://img.shields.io/github/stars/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM?style=social)
![Forks](https://img.shields.io/github/forks/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM?style=social)

A robust, production-ready machine learning web application for real-time detection of fraudulent UPI transactions. Built with Python, Streamlit, and scikit-learn.

---

## ✨ Features
- **Real-time Fraud Detection:** Instantly flag suspicious UPI transactions.
- **Batch Prediction:** Upload CSV files for bulk fraud analysis.
- **Modern Streamlit UI:** Clean, responsive, and user-friendly interface.
- **Model Performance Metrics:** See accuracy, F1-score, and ROC-AUC in-app.
- **Input Validation:** Prevents invalid or incomplete submissions.
- **Recent Predictions Table:** Track your latest checks.
- **Comprehensive Error Handling:** User-friendly error messages throughout.

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM.git
cd UPI-FRAUD-DETECTION-SYSTEM
pip install -r webapp/requirements.txt
```

### 2. Launch the App
```bash
cd webapp
streamlit run main.py
```

### 3. Predict Fraud
- **Single Transaction:** Fill out the form and click **Predict**.
- **Batch Prediction:** Upload a CSV with the required columns and download results.

---

## 🏗️ Project Structure
```
UPI-FRAUD-DETECTION-SYSTEM/
├── Copy of Sample_DATA.csv
├── Data_Analysis_for_UPI_Payment_System.ipynb
├── UPI Fraud Detection updated.pkl
├── webapp/
│   ├── app.py
│   ├── main.py
│   ├── requirements.txt
│   ├── run_production.py
│   └── templates/
│       └── index.html
└── README.md
```

---

## 🧠 Model Training & Pipeline
- **Notebook:** `Data_Analysis_for_UPI_Payment_System.ipynb`
- **Preprocessing:**
  - Drops unnecessary columns
  - One-hot encodes categorical variables
  - Scales features with `StandardScaler`
- **Model:** Trained with Random Forest, XGBoost, and more. Best model, scaler, and feature columns saved in `UPI Fraud Detection updated.pkl`.

---

## 📊 Model Performance
| Model                | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|----------------------|----------|-----------|--------|----------|---------|
| XGBoost (Optimized)  | 95.38%   | 100.00%   | 81.25% | 89.66%   | 90.63%  |
| Random Forest        | 95.38%   | 93.33%    | 87.50% | 90.32%   | 92.73%  |
| Gradient Boosting    | 93.85%   | 92.86%    | 81.25% | 86.67%   | 89.60%  |
| Decision Tree        | 84.62%   | 66.67%    | 75.00% | 70.59%   | 81.38%  |

---

## 📂 Input Data Format
- **Single Prediction:** Use the form fields in the app.
- **Batch Prediction:** CSV must match the columns used in model training (see notebook for details).

---

## 📝 Notes
- Ensure your input data matches the columns and preprocessing used during model training.
- Retrain and resave the model if you add new features or categories.
- For best results, use the provided notebook for data analysis and model retraining.

---

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

---

## 📧 Contact
For questions or support, open an issue on GitHub.

---

## 🪪 License
MIT License