# 🧠 Stroke Prediction using Machine Learning 🏥

![Python](https://img.shields.io/badge/python-3.11%2B-blue) ![ML](https://img.shields.io/badge/ML-Prediction-green) ![Status](https://img.shields.io/badge/Status-Completed-success)


🔍 A comprehensive, AI-powered project designed to predict the likelihood of a stroke using medical and demographic data. This work emphasizes the importance of early risk detection, data quality, and model robustness, which are vital in proactive healthcare. 🛡️


## 📌 Problem Statement 🎯

⚠️ Stroke (ischemic or hemorrhagic) is a leading health concern exacerbated by lifestyle diseases and an aging population. Traditional models are limited by linear assumptions and poor handling of heterogeneous data.

**Our goal:** 🎯  
🤖 Build an AI-powered pipeline that leverages patient demographics, medical history, and lifestyle data to proactively predict stroke risk.


## 🚀 Key Features ✨

- 📊 Advanced Exploratory Data Analysis (EDA)
- 🧹 Rigorous data cleaning and feature engineering
- 🔄 Multiple machine learning models benchmarked
- ⚖️ SMOTE & cost-sensitive learning for class imbalance
- 🏆 High-performance Naïve Bayes model
- 📏 Calibration, fairness, and performance diagnostics
- 🌐 Developed an interactive web application for stroke risk assessment
- 📝 Reproducible pipeline with clear documentation

### 📊 Webapp Demo 🖥️

![Webapp Gif](web_app/img/webapp.gif)

🔗 [Webapp Deployed Link](https://stroke-prediction-webapp-2bax67v4gloepsd7tqiac8.streamlit.app/) 🌐

- 🖥️ **Webapp Deployment**: Deployed Using Streamlit Cloud ☁️


## 🧪 Methodology 📋

### 1. Data Acquisition & Preprocessing 📥
- 📁 Public dataset with 5,110 patient records and 12 original features
- 🧩 Missing values imputed using KNN
- 📉 Outliers handled via winsorization and scaling
- 🏷️ Categorical variables encoded using One-Hot and Binary Encoding
- 🔢 Final feature space: 28 engineered features

### 2. Exploratory Data Analysis (EDA) 🔍
- 👵 Age, glucose level, hypertension, and heart disease are leading stroke predictors
- 📊 Strong associations validated via statistical hypothesis testing
- 📈 Bivariate plots, correlation heatmaps, and chi-squared tests used

### 3. Feature Engineering ⚙️
- 🔄 Created polynomial and interaction terms (e.g., Age × Hypertension)
- 🔗 Captured complex nonlinear relationships to improve model learnability
- 📏 Standardized all continuous features

### 4. Model Development 🤖
- 🧠 Models evaluated: Naïve Bayes, Random Forest, Logistic Regression, XGBoost
- ⚖️ Techniques for imbalance: SMOTE, weighted loss functions
- 🏆 Final model: **Naïve Bayes + SMOTE**, selected for balance of accuracy and interpretability

### 5. Evaluation 📊
- 📏 Metrics: ROC AUC, Precision, Recall, F1-score, AUPRC
- 🎯 Achieved AUC ≥ 0.8
- ⚖️ Included model calibration and fairness assessment across subgroups

## 📊 Results 🏆

| Metric          | Value (Naïve Bayes + SMOTE) |
|---------------- |-----------------------------|
| Accuracy        | High ✅                     |
| ROC AUC         | ≥ 0.8 📈                    |
| Recall (Stroke) | High sensitivity 🔍          |
| F1 Score        | Balanced performance ⚖️      |

## 💡 Key Insights 🔎

- 👵 **Age** is the most dominant risk factor for stroke.
- ❤️ **Hypertension** and **heart disease** significantly elevate risk.
- 📏 **BMI** and **glucose level** offer additional predictive power.
- 🚬 **Smoking status** shows meaningful stratification of risk.
- ⚖️ Severe **class imbalance** (19.5:1) requires targeted mitigation strategies.

## 🗂️ Project Folder Structure

```
Module1_FinalProject/
├── Final_Notebooks/     # Jupyter notebooks with analysis and model development
│   ├── 01_data_loading_and_quality.ipynb           # Data loading and quality assessment
│   ├── 02_hypothesis_testing.ipynb                 # Statistical hypothesis testing
│   ├── 03_feature_engineering.ipynb                # Feature creation and transformation
│   ├── 04_model_training_48_models.ipynb           # Main model training notebook
│   ├── 04_model_training_part_2_24_models.ipynb    # Additional model training
│   ├── 05_Final_Model_Analysis_Naive_Bayes_SMOTE.ipynb  # Final model analysis
│   ├── 05_Part2_Naive_Bayes_SMOTE_PRAUC_metrics_added.ipynb  # Extended metrics
│   ├── 06_model_prediction_validation.ipynb        # Model validation
│   └── 07_model_calibration.ipynb                  # Model calibration analysis
├── data/               # Dataset files
├── web_app/            # Web application for stroke prediction
├── .git/               # Git repository data
├── .gitattributes      # Git attributes file
├── LICENSE             # MIT License file
└── README.md           # Project documentation
```


## 👥 Contributors 🌟
1. 👨‍💻 Prashant Khare - https://github.com/sentinel1282
2. 👨‍💻 Riyaz Khorasi - https://github.com/Riyazmk1995
3. 👨‍💻 Sourangshu Pal - https://github.com/sourangshupal

## 📚 References 📖
- 🏥 World Health Organization (WHO) and Centers for Disease Control and Prevention (CDC) reports on global stroke burden and epidemiology.
- 📊 Original Dataset Source: https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset/data

## 📄 License 📝

This project is licensed under the **MIT License** ⚖️  
You are free to use, modify, and distribute this software with proper attribution.

Please take a look at the full license in the [LICENSE](LICENSE) file.

© 2025 Group 2 — Prashant Khare, Riyaz Khorasi, Sourangshu Pal. All rights reserved. 🔒

---

## 🤝 Contributing 🌱

We welcome contributions from the community to make this project even better! 🚀

If you'd like to contribute:

1. 🍴 **Fork** the repository
2. 🌿 **Create a branch** (`git checkout -b feature/your-feature`)
3. 💾 **Commit your changes** (`git commit -am 'Add your feature'`)
4. 📤 **Push to the branch** (`git push origin feature/your-feature`)
5. 📩 **Open a Pull Request**

Please ensure your code is clean, documented, and passes any existing tests (if applicable). ✨

---

⭐ If you like this project, **give it a star** and **fork it** to support and build on it! 🚀 💫


