# EXACT feature_engineering.py
# Generated from feature_summary.csv with the exact 26 feature names

import pandas as pd
import numpy as np
from typing import Dict, List

class FixedFeatureEngineer:
    """Feature Engineer with exact feature names from feature_summary.csv"""
    
    def __init__(self):
        """Initialize with the EXACT 26 feature names from training."""
        self.feature_names = [
        'age_diabetes',
        'cv_risk_count',
        'age_decade',
        'work_stress_level',
        'hypertension_elderly',
        'high_stress_work',
        'hypertension',
        'married',
        'male_age_interaction',
        'bmi_hypertension',
        'age_hypertension_diabetes',
        'bmi_glucose',
        'heart_disease',
        'bmi',
        'age_high_risk',
        'glucose_heart_disease',
        'avg_glucose_level',
        'gender_female',
        'female_elderly',
        'age_hypertension',
        'age_obesity',
        'age',
        'gender_male',
        'gender_Other',
        'modifiable_risk_count',
        'bmi_diabetes'
    ]
        
        print(f"✅ FixedFeatureEngineer initialized with {len(self.feature_names)} exact features")
    
    def engineer_features(self, patient_data: Dict) -> List[float]:
        """Create features matching the exact training order."""
        
        # Extract basic patient data
        age = float(patient_data.get('age', 50))
        hypertension = int(patient_data.get('hypertension', 0))
        heart_disease = int(patient_data.get('heart_disease', 0))
        avg_glucose_level = float(patient_data.get('avg_glucose_level', 100))
        bmi = float(patient_data.get('bmi', 25))
        
        # Handle gender
        gender = patient_data.get('gender', 'Male')
        gender_male = 1 if gender == 'Male' else 0
        gender_female = 1 if gender == 'Female' else 0
        
        # Handle marriage
        ever_married = patient_data.get('ever_married', 'Yes')
        married = 1 if ever_married == 'Yes' else 0
        
        # Handle work type
        work_type = patient_data.get('work_type', 'Private')
        
        # Handle residence type
        residence_type = patient_data.get('Residence_type', 'Urban')
        
        # Handle smoking status
        smoking_status = patient_data.get('smoking_status', 'never_smoked')
        
        # Calculate derived indicators
        diabetes_indicator = 1 if avg_glucose_level > 125 else 0
        elderly_indicator = 1 if age >= 65 else 0
        obesity_indicator = 1 if bmi >= 30 else 0
        
        # Create comprehensive feature mapping for ALL possible features
        feature_mapping = {
            # Basic demographic features
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'avg_glucose_level': avg_glucose_level,
            'bmi': bmi,
            
            # Gender features
            'gender_male': 1 if gender == 'Male' else 0,
            'gender_female': 1 if gender == 'Female' else 0,
            'gender_Male': 1 if gender == 'Male' else 0,  # For backward compatibility
            'gender_Female': 1 if gender == 'Female' else 0,  # For backward compatibility
            'gender_Other': 1 if gender not in ['Male', 'Female'] else 0,
            
            # Marriage features
            'married': married,
            'ever_married_Yes': float(married),
            'ever_married_No': float(1 - married),
            
            # Work type features
            'work_type_Private': 1.0 if work_type == 'Private' else 0.0,
            'work_type_Self-employed': 1.0 if work_type == 'Self-employed' else 0.0,
            'work_type_Govt_job': 1.0 if work_type == 'Govt_job' else 0.0,
            'work_type_children': 1.0 if work_type == 'children' else 0.0,
            'work_type_Never_worked': 1.0 if work_type == 'Never_worked' else 0.0,
            
            # Residence type features
            'Residence_type_Urban': 1.0 if residence_type == 'Urban' else 0.0,
            'Residence_type_Rural': 1.0 if residence_type == 'Rural' else 0.0,
            
            # Smoking status features
            'smoking_status_never smoked': 1.0 if 'never' in smoking_status else 0.0,
            'smoking_status_formerly smoked': 1.0 if 'formerly' in smoking_status else 0.0,
            'smoking_status_smokes': 1.0 if smoking_status == 'smokes' else 0.0,
            'smoking_status_Unknown': 1.0 if smoking_status == 'Unknown' else 0.0,
            
            # Age-based engineered features
            'age_decade': age / 10.0,
            'age_high_risk': float(elderly_indicator),
            'age_squared': age * age,
            
            # Risk count features
            'cv_risk_count': float(hypertension + heart_disease + diabetes_indicator + obesity_indicator),
            'modifiable_risk_count': float(hypertension + diabetes_indicator + obesity_indicator),
            
            # Interaction features
            'hypertension_elderly': float(hypertension * elderly_indicator),
            'female_elderly': float(gender_female * elderly_indicator),
            'male_elderly': float(gender_male * elderly_indicator),
            'male_age_interaction': float(gender_male * age),
            'female_age_interaction': float(gender_female * age),
            'age_hypertension': float(age * hypertension),
            'age_heart_disease': float(age * heart_disease),
            'bmi_hypertension': float(bmi * hypertension),
            'bmi_heart_disease': float(bmi * heart_disease),
            'glucose_heart_disease': float(avg_glucose_level * heart_disease),
            'glucose_hypertension': float(avg_glucose_level * hypertension),
            'age_hypertension_diabetes': float(age * hypertension * diabetes_indicator),
            'bmi_glucose': float(bmi * avg_glucose_level),
            'age_obesity': float(age * obesity_indicator),
            'bmi_diabetes': float(bmi * diabetes_indicator),
            'age_diabetes': float(age * diabetes_indicator),
            
            # BMI categories
            'bmi_normal': 1.0 if 18.5 <= bmi < 25 else 0.0,
            'bmi_overweight': 1.0 if 25 <= bmi < 30 else 0.0,
            'bmi_obese': 1.0 if bmi >= 30 else 0.0,
            'bmi_underweight': 1.0 if bmi < 18.5 else 0.0,
            
            # Glucose categories
            'glucose_normal': 1.0 if avg_glucose_level < 100 else 0.0,
            'glucose_prediabetic': 1.0 if 100 <= avg_glucose_level <= 125 else 0.0,
            'glucose_diabetic': 1.0 if avg_glucose_level > 125 else 0.0,
            
            # Age categories
            'age_young': 1.0 if age < 45 else 0.0,
            'age_middle': 1.0 if 45 <= age < 65 else 0.0,
            'age_elderly': 1.0 if age >= 65 else 0.0,
            
            # Work-related features
            'work_stress_level': 2.0,  # Default medium stress
            'high_stress_work': 0.0,   # Default no high stress
            
            # Complex interactions
            'age_bmi_interaction': age * bmi,
            'glucose_age_interaction': avg_glucose_level * age,
            'hypertension_heart_disease': float(hypertension * heart_disease),
            
            # Risk scores
            'cardiovascular_risk_score': float(age/10 + hypertension*2 + heart_disease*3 + diabetes_indicator*2),
            'metabolic_risk_score': float(bmi/5 + avg_glucose_level/50 + diabetes_indicator*3),
        }
        
        # Create feature vector in EXACT order from CSV
        features = []
        for feature_name in self.feature_names:
            if feature_name in feature_mapping:
                features.append(float(feature_mapping[feature_name]))
            else:
                # Unknown feature - set to 0 and warn
                print(f"⚠️ Unknown feature '{feature_name}' set to 0.0")
                features.append(0.0)
        
        print(f"🔧 Created {len(features)} features in exact CSV order")
        return features
    
    def create_feature_dataframe(self, patient_data: Dict) -> pd.DataFrame:
        """Create features as DataFrame with exact feature names from CSV."""
        # Instead of using the feature_names list which might be in the wrong order,
        # we'll create a dictionary of all possible features and then select only what we need
        # in the exact order the model expects
        
        # Get all possible features
        all_features = self.get_all_features(patient_data)
        
        # Define the exact feature order expected by the model
        # This is the critical part - these must match exactly what the model was trained with
        # We're combining features from feature_summary.csv and additional features the model expects
        expected_feature_order = [
            'age_diabetes',
            'cv_risk_count',
            'age_decade',
            'work_stress_level',
            'hypertension_elderly',
            'high_stress_work',
            'hypertension',
            'married',
            'male_age_interaction',
            'bmi_hypertension',
            'age_hypertension_diabetes',
            'bmi_glucose',
            'heart_disease',
            'bmi',
            'age_high_risk',
            'glucose_heart_disease',
            'avg_glucose_level',
            'gender_female',
            'female_elderly',
            'age_hypertension',
            'age_obesity',
            'age',
            'gender_male',
            'modifiable_risk_count',
            'bmi_diabetes',
            # Additional features required by the model but not in CSV
            'gender_Male',
            'gender_Other'
        ]
        
        print(f"✅ Using {len(expected_feature_order)} features including gender_Male and gender_Other")
        
        # Create a new DataFrame with features in the exact expected order
        ordered_features = []
        for feature_name in expected_feature_order:
            if feature_name in all_features:
                ordered_features.append(all_features[feature_name])
            else:
                print(f"⚠️ Missing expected feature: {feature_name}, setting to 0")
                ordered_features.append(0.0)
        
        # Create DataFrame with the exact feature order
        df = pd.DataFrame([ordered_features], columns=expected_feature_order)
        
        # Debug information
        print(f"🔍 DataFrame columns: {df.columns.tolist()}")
        print(f"🔍 gender_Male present: {'gender_Male' in df.columns}")
        print(f"🔍 Number of features: {len(df.columns)}")
        
        return df
        
    def get_all_features(self, patient_data: Dict) -> Dict:
        """Get all possible features as a dictionary."""
        # Extract basic patient data
        age = float(patient_data.get('age', 65))
        gender = patient_data.get('gender', 'Male')
        hypertension = int(patient_data.get('hypertension', 0))
        heart_disease = int(patient_data.get('heart_disease', 0))
        ever_married = patient_data.get('ever_married', 'Yes')
        work_type = patient_data.get('work_type', 'Private')
        residence_type = patient_data.get('residence_type', 'Urban')
        avg_glucose_level = float(patient_data.get('avg_glucose_level', 100))
        bmi = float(patient_data.get('bmi', 25))
        smoking_status = patient_data.get('smoking_status', 'never_smoked')
        
        # Derived indicators
        diabetes_indicator = 1 if avg_glucose_level > 125 else 0
        elderly_indicator = 1 if age >= 65 else 0
        obesity_indicator = 1 if bmi >= 30 else 0
        
        # Gender features - ensure correct case for gender_Male
        gender_male = 1 if gender == 'Male' else 0
        gender_female = 1 if gender == 'Female' else 0
        gender_Male = 1 if gender == 'Male' else 0  # Exact case match
        gender_Other = 1 if gender not in ['Male', 'Female'] else 0
        
        # Marriage features
        married = 1 if ever_married == 'Yes' else 0
        
        # Create a comprehensive dictionary of all possible features
        all_features = {
            # Basic features
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'avg_glucose_level': avg_glucose_level,
            'bmi': bmi,
            'gender_male': gender_male,
            'gender_Male': gender_Male,  # Ensure exact case match
            'gender_female': gender_female,
            'gender_Other': gender_Other,
            'married': married,
            
            # Age-based features
            'age_decade': age / 10.0,
            'age_high_risk': float(elderly_indicator),
            
            # Risk count features
            'cv_risk_count': float(hypertension + heart_disease + diabetes_indicator + obesity_indicator),
            'modifiable_risk_count': float(hypertension + diabetes_indicator + obesity_indicator),
            
            # Interaction features
            'hypertension_elderly': float(hypertension * elderly_indicator),
            'female_elderly': float(gender_female * elderly_indicator),
            'male_age_interaction': float(gender_male * age),
            'age_hypertension': float(age * hypertension),
            'bmi_hypertension': float(bmi * hypertension),
            'glucose_heart_disease': float(avg_glucose_level * heart_disease),
            'age_hypertension_diabetes': float(age * hypertension * diabetes_indicator),
            'bmi_glucose': float(bmi * avg_glucose_level),
            'age_obesity': float(age * obesity_indicator),
            'bmi_diabetes': float(bmi * diabetes_indicator),
            'age_diabetes': float(age * diabetes_indicator),
            
            # Work-related features
            'work_stress_level': 2.0,  # Default medium stress
            'high_stress_work': 0.0    # Default no high stress
        }
        
        return all_features
    
    def validate_features(self, features: List[float]) -> bool:
        """Validate feature count and values."""
        if len(features) != len(self.feature_names):
            print(f"❌ Feature count mismatch: {len(features)} vs {len(self.feature_names)}")
            return False
        
        for i, f in enumerate(features):
            if not isinstance(f, (int, float, bool)) or np.isnan(f) or np.isinf(f):
                print(f"❌ Invalid feature {i} ({self.feature_names[i]}): {f}")
                return False
        
        print(f"✅ All {len(features)} features valid")
        return True

# Backward compatibility
FeatureEngineer = FixedFeatureEngineer

# Test function
def test_exact_feature_engineer():
    """Test the feature engineer with exact CSV features."""
    
    print("🧪 TESTING EXACT FEATURE ENGINEER")
    print("-" * 35)
    
    fe = FixedFeatureEngineer()
    
    # Test patient
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
    
    try:
        # Create features
        features_df = fe.create_feature_dataframe(test_patient)
        print(f"✅ Features created: {features_df.shape}")
        
        # Validate
        features_list = fe.engineer_features(test_patient)
        is_valid = fe.validate_features(features_list)
        
        if is_valid:
            print(f"✅ Feature validation passed")
            return features_df
        else:
            print(f"❌ Feature validation failed")
            return None
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_exact_feature_engineer()
