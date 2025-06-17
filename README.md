UPI Fraud Detection System 🚨

![GitHub repo size](https://img.shields.io/github/repo-size/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM)
![GitHub contributors](https://img.shields.io/github/contributors/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM)
![GitHub stars](https://img.shields.io/github/stars/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM?style=social)
![GitHub forks](https://img.shields.io/github/forks/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM?style=social)

## 🔧 Latest Updates (v2.0)

**Major Issues Resolved!** ✅
- ✅ Fixed SettingWithCopyWarning in pandas operations
- ✅ Resolved IndentationError and code structure issues
- ✅ Fixed package version conflicts (scikit-learn, XGBoost, imbalanced-learn)
- ✅ Corrected variable naming inconsistencies
- ✅ Enhanced error handling and code robustness
- ✅ Improved model evaluation and hyperparameter tuning
- ✅ Added comprehensive documentation and comments

## Introduction 📖

Welcome to the UPI Fraud Detection System! This repository is dedicated to detecting fraudulent activities in Unified Payments Interface (UPI) transactions. The system leverages machine learning techniques to identify suspicious transactions in real-time.

**New Fixed Notebook**: `Data_Analysis_for_UPI_Payment_Systems_Fixed.ipynb` - Contains all resolved issues and improved implementation.

Features ✨

Real-time Fraud Detection: Monitors transactions in real-time and flags suspicious activities. This ensures immediate action can be taken to prevent fraudulent transactions.

Machine Learning Models: Utilizes advanced ML algorithms to predict fraudulent behavior. These models are trained on historical transaction data to identify patterns indicative of fraud.

User-Friendly Interface: Easy-to-use interface for managing and reviewing flagged transactions. This interface allows users to quickly assess and act on potential fraud cases.

Scalable Architecture: Designed to handle large volumes of transactions efficiently. The system can scale horizontally to manage increased transaction loads without performance degradation.

Repository Structure 🗂️

```
UPI-FRAUD-DETECTION-SYSTEM/
├── Data_Analysis_for_UPI_Payment_Systems (1).ipynb  # Original notebook (has issues)
├── Data_Analysis_for_UPI_Payment_Systems_Fixed.ipynb  # ✅ Fixed notebook (recommended)
├── Copy of Sample_DATA.csv                           # Dataset
├── UPI Fraud Detection updated.pkl                  # Original model
├── UPI_Fraud_Detection_Model_Fixed.pkl             # ✅ Improved model
├── requirements.txt                                 # ✅ Fixed package dependencies
└── README.md                                       # This file
```

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM.git
cd UPI-FRAUD-DETECTION-SYSTEM

# Install required packages
pip install -r requirements.txt
```

### Usage
1. Open the **fixed notebook**: `Data_Analysis_for_UPI_Payment_Systems_Fixed.ipynb`
2. Run all cells sequentially
3. The notebook will automatically handle data loading, preprocessing, and model training

## 🔧 Issues Resolved

### Critical Fixes ✅

1. **SettingWithCopyWarning Resolution**
   - **Issue**: Pandas warning when modifying dataframe slices
   - **Fix**: Used `.copy()` method for dataframe operations
   - **Impact**: Eliminated warnings and potential data corruption

2. **IndentationError Correction**
   - **Issue**: Inconsistent indentation causing syntax errors
   - **Fix**: Standardized 4-space indentation throughout
   - **Impact**: Code now runs without syntax errors

3. **Package Version Conflicts**
   - **Issue**: Incompatible scikit-learn, XGBoost, and imbalanced-learn versions
   - **Fix**: Updated `requirements.txt` with compatible versions
   - **Impact**: All packages work together seamlessly

4. **Variable Naming Inconsistencies**
   - **Issue**: Mixed use of `Y_train`/`y_train` and `Y_test`/`y_test`
   - **Fix**: Standardized to lowercase convention
   - **Impact**: Eliminated NameError exceptions

5. **Duplicate Function Definitions**
   - **Issue**: Multiple definitions of `evaluate_model()` function
   - **Fix**: Consolidated into single, robust implementation
   - **Impact**: Cleaner code and consistent behavior

### Enhancements 🚀

1. **Comprehensive Error Handling**
   - Added try-catch blocks for robust execution
   - Graceful handling of missing files and data issues

2. **Improved Model Evaluation**
   - Enhanced metrics calculation with zero-division protection
   - Added cross-validation and hyperparameter tuning

3. **Better Visualization**
   - Fixed plotting issues and improved chart aesthetics
   - Added comprehensive performance comparison charts

4. **Code Documentation**
   - Added detailed comments and docstrings
   - Improved markdown documentation

## 📊 Model Performance (Fixed Version)

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| XGBoost (Optimized) | 95.38% | 100.00% | 81.25% | 89.66% | 90.63% |
| Random Forest | 95.38% | 93.33% | 87.50% | 90.32% | 92.73% |
| Gradient Boosting | 93.85% | 92.86% | 81.25% | 86.67% | 89.60% |
| Decision Tree | 84.62% | 66.67% | 75.00% | 70.59% | 81.38% |

Notebooks: Jupyter notebooks containing the data analysis and model training processes. These notebooks provide a detailed look at how the data is processed and how the models are built and evaluated.

Data: Sample datasets used for training and testing the models. These datasets are essential for replicating the results and for further experimentation.

Scripts: Python scripts for data preprocessing, model training, and evaluation. These scripts automate the tasks of preparing data, training models, and evaluating their performance.

Docs: Documentation and resources related to the project. This includes detailed descriptions of the methods used and guides for using the system.

Tests: Unit tests to ensure the reliability of the system. These tests verify that the different components of the system work as expected and help prevent regression issues.

Future Updates 🚀

Enhanced Detection Algorithms: Incorporating deep learning models for improved accuracy. Future iterations will explore more sophisticated techniques to better identify fraud.

Integration with UPI Networks: Direct integration with UPI networks for seamless operation. This will allow the system to directly monitor and analyze transactions from the UPI network.

Mobile App: Developing a mobile application for on-the-go monitoring. Users will be able to receive alerts and manage fraud detection from their mobile devices.

User Feedback Loop: Implementing a feedback system to continuously improve the detection algorithms. User feedback will be used to fine-tune the models and improve their accuracy over time.

How to Contribute 🤝

We welcome contributions from the community! Follow these steps to contribute:

1. Fork the Repository: Click on the fork button at the top right corner.

2. Clone the Repository:
```
git clone https://github.com/KunjShah95/UPI-FRAUD-DETECTION-SYSTEM.git
```
3. Create a Branch:
```
git checkout -b feature-branch
```
4. Make Your Changes:
Implement your feature or fix a bug.
5. Commit and Push:
```
git commit -m "Your commit message"
git push origin feature-branch
```
6. Create a Pull Request:
Go to the repository on GitHub and create a pull request.

Contact 📧

For any queries or issues, feel free to reach out to us via GitHub Issues.

