
STROKE PREDICTION MODEL SUMMARY
================================
Model Type: Naive Bayes with SMOTE
Training Date: 2025-06-20 12:07:45
Performance: ROC-AUC = 0.8125

Key Files:
- Model: stroke_prediction_nb_smote.pkl
- Features: feature_names.json  
- Metadata: model_metadata.json
- Importance: feature_importance.csv

To use this model for predictions:
1. Load the model using joblib.load()
2. Ensure input features match feature_names.json
3. Use model.predict_proba() for risk scores
