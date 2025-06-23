import joblib
import numpy as np
import pandas as pd
import streamlit as st
import warnings
from typing import Dict, Tuple, List

# Suppress StandardScaler feature name warnings
warnings.filterwarnings('ignore', message='.*feature names.*')
warnings.filterwarnings('ignore', message='.*StandardScaler.*')

# Import the fixed feature engineer
from src.feature_engineering_exact import FixedFeatureEngineer

# Move the cached function outside the class to avoid 'self' hashing issues
@st.cache_resource
def load_model(model_path: str):
    """Load calibrated model with caching for performance"""
    try:
        # Load model using joblib (preferred for scikit-learn models)
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

class ModelHandler:
    def __init__(self, model_path="models/stroke_prediction_calibrated.pkl"):
        """Initialize the ModelHandler with the calibrated model and fixed feature engineer."""
        
        # Use the cached function instead of a cached method
        self.model = load_model(model_path)
        
        # Use the FIXED feature engineer that creates proper DataFrame output
        self.feature_engineer = FixedFeatureEngineer()
        
        # Store model path for reference
        self.model_path = model_path
        
        if self.model is not None:
            print(f"✅ Model loaded successfully from: {model_path}")
            print(f"✅ Using FixedFeatureEngineer with {len(self.feature_engineer.feature_names)} features")
        else:
            print(f"❌ Failed to load model from: {model_path}")
    
    def predict_stroke_risk(self, patient_data: Dict) -> Tuple[float, str, Dict]:
        """Generate stroke risk prediction with clinical interpretation"""
        
        if self.model is None:
            raise Exception("Model not loaded properly")
        
        try:
            # Engineer features as DataFrame with proper column names (fixes StandardScaler warnings)
            features_df = self.feature_engineer.create_feature_dataframe(patient_data)
            
            # Debug information (can be removed in production)
            print(f"🎯 Model input shape: {features_df.shape}")
            print(f"🎯 Model input columns: {len(features_df.columns)} features")
            print(f"🎯 Model input range: {features_df.values.min():.3f} to {features_df.values.max():.3f}")
            
            # Get calibrated probability (DataFrame maintains feature names for StandardScaler)
            probabilities = self.model.predict_proba(features_df)
            probability = probabilities[0, 1]  # Stroke probability (class 1)
            
            print(f"🎯 Raw probabilities: {probabilities[0]}")
            print(f"🎯 Stroke probability: {probability:.6f} ({probability*100:.1f}%)")
            
            # Risk classification
            risk_level = self._classify_risk(probability)
            
            # Feature importance (simplified version)
            feature_importance = self._get_feature_importance(features_df.iloc[0].to_dict(), patient_data)
            
            return probability, risk_level, feature_importance
            
        except Exception as e:
            print(f"❌ Prediction failed in ModelHandler: {e}")
            import traceback
            traceback.print_exc()
            raise e
    
    def _classify_risk(self, probability: float) -> str:
        """Classify risk level based on calibrated probability"""
        if probability < 0.10:
            return "Low Risk"
        elif probability < 0.30:
            return "Moderate Risk"
        elif probability < 0.60:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def _get_feature_importance(self, features_dict: Dict, patient_data: Dict) -> Dict[str, float]:
        """Get simplified feature importance for interpretation"""
        
        # Define key features and their relative importance weights
        # This is a simplified version - in production you might use SHAP or similar
        age = patient_data.get('age', 50)
        hypertension = patient_data.get('hypertension', 0)
        heart_disease = patient_data.get('heart_disease', 0)
        avg_glucose_level = patient_data.get('avg_glucose_level', 100)
        bmi = patient_data.get('bmi', 25)
        smoking_status = patient_data.get('smoking_status', 'never_smoked')
        gender = patient_data.get('gender', 'Male')
        ever_married = patient_data.get('ever_married', 'Yes')
        
        feature_weights = {
            'age': min(age / 100.0, 0.35),  # Normalize age contribution (max 35%)
            'hypertension': 0.15 if hypertension == 1 else 0.0,
            'heart_disease': 0.20 if heart_disease == 1 else 0.0,
            'avg_glucose_level': min(avg_glucose_level / 200.0, 0.25),  # Normalize glucose (max 25%)
            'bmi': 0.15 if bmi > 30 else 0.10 if bmi > 25 else 0.05,
            'smoking_status': 0.15 if 'smokes' in smoking_status else 
                            0.05 if 'formerly' in smoking_status else 0.0,
            'gender': 0.05 if gender == 'Male' else 0.02,
            'ever_married': 0.03 if ever_married == 'Yes' else 0.0
        }
        
        # Normalize to sum to 1.0
        total_weight = sum(feature_weights.values())
        if total_weight > 0:
            feature_weights = {k: v/total_weight for k, v in feature_weights.items()}
        
        return feature_weights
    
    def get_model_info(self) -> Dict:
        """Get model information for display"""
        if self.model is None:
            return {"status": "Model not loaded"}
        
        try:
            # Try to get model information
            model_type = type(self.model).__name__
            
            # Check if it's a pipeline and get the final estimator
            if hasattr(self.model, 'named_steps'):
                final_estimator = None
                for step_name, step in self.model.named_steps.items():
                    if hasattr(step, 'predict_proba'):
                        final_estimator = type(step).__name__
                        break
                if final_estimator:
                    model_type = f"Pipeline with {final_estimator}"
            
            return {
                "status": "Model loaded successfully",
                "model_type": model_type,
                "model_path": self.model_path,
                "features_count": len(self.feature_engineer.feature_names),
                "feature_engineer": "FixedFeatureEngineer",
                "calibrated": "Yes" if "calibrated" in self.model_path else "Unknown"
            }
        except Exception as e:
            return {"status": f"Error getting model info: {e}"}
    
    def validate_prediction_inputs(self, patient_data: Dict) -> Tuple[bool, List[str]]:
        """Validate inputs before prediction"""
        errors = []
        
        required_fields = [
            'age', 'gender', 'hypertension', 'heart_disease', 
            'ever_married', 'work_type', 'Residence_type', 
            'avg_glucose_level', 'bmi', 'smoking_status'
        ]
        
        # Check for missing fields
        for field in required_fields:
            if field not in patient_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate ranges
        if 'age' in patient_data:
            if not (18 <= patient_data['age'] <= 120):
                errors.append("Age must be between 18 and 120 years")
        
        if 'bmi' in patient_data:
            if not (10.0 <= patient_data['bmi'] <= 70.0):
                errors.append("BMI must be between 10.0 and 70.0")
        
        if 'avg_glucose_level' in patient_data:
            if not (50.0 <= patient_data['avg_glucose_level'] <= 400.0):
                errors.append("Glucose level must be between 50.0 and 400.0 mg/dL")
        
        # Validate categorical fields
        if 'gender' in patient_data:
            if patient_data['gender'] not in ['Male', 'Female']:
                errors.append("Gender must be 'Male' or 'Female'")
        
        if 'ever_married' in patient_data:
            if patient_data['ever_married'] not in ['Yes', 'No']:
                errors.append("Ever married must be 'Yes' or 'No'")
        
        if 'hypertension' in patient_data:
            if patient_data['hypertension'] not in [0, 1]:
                errors.append("Hypertension must be 0 or 1")
        
        if 'heart_disease' in patient_data:
            if patient_data['heart_disease'] not in [0, 1]:
                errors.append("Heart disease must be 0 or 1")
        
        return len(errors) == 0, errors
    
    def create_risk_summary(self, patient_data: Dict, probability: float, risk_level: str) -> Dict:
        """Create a comprehensive risk summary for clinical use"""
        
        # Calculate risk factors present
        risk_factors = []
        
        if patient_data.get('age', 0) >= 65:
            risk_factors.append("Advanced age (≥65 years)")
        
        if patient_data.get('hypertension', 0) == 1:
            risk_factors.append("Hypertension")
        
        if patient_data.get('heart_disease', 0) == 1:
            risk_factors.append("Heart disease")
        
        if patient_data.get('avg_glucose_level', 0) > 125:
            risk_factors.append("Diabetes/Pre-diabetes")
        
        if patient_data.get('bmi', 0) >= 30:
            risk_factors.append("Obesity")
        elif patient_data.get('bmi', 0) >= 25:
            risk_factors.append("Overweight")
        
        smoking = patient_data.get('smoking_status', 'never_smoked')
        if 'smokes' in smoking:
            risk_factors.append("Current smoking")
        elif 'formerly' in smoking:
            risk_factors.append("Former smoking")
        
        # Clinical recommendations based on risk level
        if 'Very High' in risk_level:
            recommendations = [
                "Immediate cardiovascular evaluation recommended",
                "Consider specialist referral (cardiology/neurology)",
                "Aggressive risk factor modification",
                "Close monitoring and follow-up"
            ]
        elif 'High' in risk_level:
            recommendations = [
                "Comprehensive cardiovascular assessment",
                "Intensive risk factor management",
                "Regular monitoring",
                "Consider specialist consultation"
            ]
        elif 'Moderate' in risk_level:
            recommendations = [
                "Risk factor modification program",
                "Regular health monitoring",
                "Lifestyle interventions",
                "Periodic reassessment"
            ]
        else:  # Low Risk
            recommendations = [
                "Continue healthy lifestyle practices",
                "Regular health check-ups",
                "Maintain current preventive measures",
                "Monitor for new risk factors"
            ]
        
        return {
            'probability': probability,
            'probability_percent': probability * 100,
            'risk_level': risk_level,
            'risk_factors_present': risk_factors,
            'risk_factor_count': len(risk_factors),
            'recommendations': recommendations,
            'assessment_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }

# Quick test function for development
def test_model_handler():
    """Test function to verify ModelHandler is working correctly"""
    
    print("🧪 TESTING MODELHANDLER")
    print("=" * 30)
    
    try:
        # Initialize handler
        handler = ModelHandler()
        
        # Test with the problematic patient that was showing 0.1%
        test_patient = {
            'age': 77.0,
            'gender': 'Male',
            'hypertension': 1,
            'heart_disease': 1,
            'ever_married': 'Yes',
            'work_type': 'Retired',
            'Residence_type': 'Urban',
            'avg_glucose_level': 236.0,
            'bmi': 36.7,
            'smoking_status': 'never_smoked'
        }
        
        print(f"👤 Testing patient: 77M, BMI 36.7, Glucose 236, HTN+HD")
        
        # Validate inputs
        is_valid, errors = handler.validate_prediction_inputs(test_patient)
        if not is_valid:
            print(f"❌ Validation errors: {errors}")
            return
        
        # Make prediction
        probability, risk_level, importance = handler.predict_stroke_risk(test_patient)
        
        # Create risk summary
        risk_summary = handler.create_risk_summary(test_patient, probability, risk_level)
        
        print(f"\n🎯 PREDICTION RESULTS:")
        print(f"   Probability: {probability:.4f} ({probability*100:.1f}%)")
        print(f"   Risk Level: {risk_level}")
        print(f"   Risk Factors: {len(risk_summary['risk_factors_present'])}")
        
        if probability > 0.05:
            print(f"   ✅ SUCCESS! Realistic prediction (was 0.1% before fix)")
        else:
            print(f"   ❌ Still too low - check model/features")
        
        # Test model info
        model_info = handler.get_model_info()
        print(f"\n📊 Model Info: {model_info['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run test when script is executed directly
    test_model_handler()