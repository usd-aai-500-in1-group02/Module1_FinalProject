# 🧠 Heart Stroke Prediction using Machine Learning

![Python](https://img.shields.io/badge/python-3.11%2B-blue)


A comprehensive, AI-powered project designed to predict the likelihood of a stroke using medical and demographic data. This work emphasizes the importance of early risk detection, data quality, and model robustness—vital in proactive healthcare.


## 🧠 Problem Statement

Stroke (ischemic or hemorrhagic) is a leading health concern exacerbated by lifestyle diseases and an aging population. Traditional models are limited by linear assumptions and poor handling of heterogeneous data.

**Our goal:**  
Build an AI-powered pipeline that leverages patient demographics, medical history, and lifestyle data to proactively predict stroke risk.


## 🚀 Key Features

- Advanced Exploratory Data Analysis (EDA)
- Rigorous data cleaning and feature engineering
- Multiple machine learning models benchmarked
- SMOTE & cost-sensitive learning for class imbalance
- High-performance Naïve Bayes model
- Calibration, fairness, and performance diagnostics
- Reproducible pipeline with clear documentation



## 🧪 Methodology

### 1. Data Acquisition & Preprocessing
- Public dataset with 5,110 patient records and 12 original features
- Missing values imputed using KNN
- Outliers handled via winsorization and scaling
- Categorical variables encoded using One-Hot and Binary Encoding
- Final feature space: 28 engineered features

### 2. Exploratory Data Analysis (EDA)
- Age, glucose level, hypertension, and heart disease are leading stroke predictors
- Strong associations validated via statistical hypothesis testing
- Bivariate plots, correlation heatmaps, and chi-squared tests used

### 3. Feature Engineering
- Created polynomial and interaction terms (e.g., Age × Hypertension)
- Captured complex nonlinear relationships to improve model learnability
- Standardized all continuous features

### 4. Model Development
- Models evaluated: Naïve Bayes, Random Forest, Logistic Regression, XGBoost
- Techniques for imbalance: SMOTE, weighted loss functions
- Final model: **Naïve Bayes + SMOTE**, selected for balance of accuracy and interpretability

### 5. Evaluation
- Metrics: ROC AUC, Precision, Recall, F1-score, AUPRC
- Achieved AUC ≥ 0.8
- Included model calibration and fairness assessment across subgroups

## 📊 Results

| Metric          | Value (Naïve Bayes + SMOTE) |
|---------------- |-----------------------------|
| Accuracy        | High                        |
| ROC AUC         | ≥ 0.8                       |
| Recall (Stroke) | High sensitivity            |
| F1 Score        | Balanced performance        |

## 💡 Key Insights

- **Age** is the most dominant risk factor for stroke.
- **Hypertension** and **heart disease** significantly elevate risk.
- **BMI** and **glucose level** offer additional predictive power.
- **Smoking status** shows meaningful stratification of risk.
- Severe **class imbalance** (19.5:1) requires targeted mitigation strategies.

## 📚 References
- World Health Organization (WHO) and Centers for Disease Control and Prevention (CDC) reports on global stroke burden and epidemiology.
- Original Dataset Source: https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset/data

