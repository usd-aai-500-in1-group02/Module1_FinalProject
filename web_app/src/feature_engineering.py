# Updated feature_engineering.py
# Fixed version that creates proper features for stroke prediction

import pandas as pd
import numpy as np
from typing import Dict, List

class FixedFeatureEngineer:
    """
    Fixed Feature Engineer that creates the correct 27 features for stroke prediction.
    
    This fixes the original issues:
    - Was creating only 1 feature instead of 27
    - Was returning DataFrame instead of list
    - Caused 0.1% predictions for all patients
    """
    
    def __init__(self):
        """Initialize with the correct feature names for your model."""
        # These should match exactly what your model was trained on
        self.feature_names = [
            'age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi',
            'gender_Male', 'gender_female', 'married',
            'age_decade', 'age_high_risk', 'cv_risk_count', 
            'hypertension_elderly', 'female_elderly', 'male_age_interaction',
            'age_hypertension', 'bmi_hypertension', 'glucose_heart_disease',
            'age_hypertension_diabetes', 'bmi_glucose', 'age_obesity',
            'bmi_diabetes', 'age_diabetes', 'modifiable_risk_count',
            'work_stress_level', 'high_stress_work', 'gender_Male', 'gender_Other'
        ]
        
        print(f"✅ FixedFeatureEngineer initialized with {len(self.feature_names)} features")
    
    def engineer_features(self, patient_data: Dict) -> List[float]:
        """
        Create engineered features from patient data.
        
        CRITICAL: This must return a LIST of 27 features, not a DataFrame!
        
        Args:
            patient_data (Dict): Patient information
            
        Returns:
            List[float]: List of 27 engineered features
        """
        
        # Extract basic features
        age = float(patient_data.get('age', 50))
        hypertension = int(patient_data.get('hypertension', 0))
        heart_disease = int(patient_data.get('heart_disease', 0))
        avg_glucose_level = float(patient_data.get('avg_glucose_level', 100))
        bmi = float(patient_data.get('bmi', 25))
        
        # Handle gender properly
        gender = patient_data.get('gender', 'Male')
        gender_Male = 1 if gender == 'Male' else 0  # Numeric for model (not boolean)
        gender_female = 1 if gender == 'Female' else 0  # Numeric for model
        gender_Other = 0  # Always 0 since we only have Male/Female
        
        # Handle marriage
        ever_married = patient_data.get('ever_married', 'Yes')
        married = 1 if ever_married == 'Yes' else 0
        
        # Calculate derived indicators
        diabetes_indicator = 1 if avg_glucose_level > 125 else 0
        elderly_indicator = 1 if age >= 65 else 0
        obesity_indicator = 1 if bmi >= 30 else 0
        
        # Create the feature vector in exact order
        features = [
            # Basic features (0-7)
            age,                                    # 0: age
            hypertension,                           # 1: hypertension
            heart_disease,                          # 2: heart_disease
            avg_glucose_level,                      # 3: avg_glucose_level
            bmi,                                    # 4: bmi
            gender_Male,                            # 5: gender_Male
            gender_female,                          # 6: gender_female
            married,                                # 7: married
            
            # Age-based features (8-9)
            age / 10.0,                            # 8: age_decade
            float(elderly_indicator),               # 9: age_high_risk
            
            # Risk count features (10)
            float(hypertension + heart_disease + diabetes_indicator + obesity_indicator),  # 10: cv_risk_count
            
            # Interaction features (11-19)
            float(hypertension * elderly_indicator),        # 11: hypertension_elderly
            float(gender_female * elderly_indicator),       # 12: female_elderly
            float(gender_Male * age),                        # 13: male_age_interaction
            float(age * hypertension),                       # 14: age_hypertension
            float(bmi * hypertension),                       # 15: bmi_hypertension
            float(avg_glucose_level * heart_disease),       # 16: glucose_heart_disease
            float(age * hypertension * diabetes_indicator), # 17: age_hypertension_diabetes
            float(bmi * avg_glucose_level),                  # 18: bmi_glucose
            float(age * obesity_indicator),                  # 19: age_obesity
            
            # More derived features (20-22)
            float(bmi * diabetes_indicator),                 # 20: bmi_diabetes
            float(age * diabetes_indicator),                 # 21: age_diabetes
            float(hypertension + diabetes_indicator + obesity_indicator),  # 22: modifiable_risk_count
            
            # Work-related features (23-24)
            2.0,                                            # 23: work_stress_level (default)
            0.0,                                            # 24: high_stress_work (default)
            
            # Gender features (25-26)
            gender_Male,                                    # 25: gender_Male
            gender_Other                                    # 26: gender_Other
        ]
        
        # CRITICAL: Ensure we return exactly the right number of features
        if len(features) != len(self.feature_names):
            raise ValueError(f"Feature count mismatch! Created {len(features)}, expected {len(self.feature_names)}")
        
        # Debug information
        print(f"🔧 Features created: {len(features)} features")
        print(f"🔧 Non-zero features: {sum(1 for f in features if f != 0)}")
        
        # CRITICAL: Return a LIST, not a DataFrame!
        return features
    
    def create_feature_dataframe(self, patient_data: Dict) -> pd.DataFrame:
        """
        Create features as a DataFrame with proper column names.
        This fixes the StandardScaler feature name warnings.
        
        Args:
            patient_data (Dict): Patient information
            
        Returns:
            pd.DataFrame: DataFrame with feature names as columns
        """
        features = self.engineer_features(patient_data)
        
        # Create DataFrame with proper feature names
        feature_df = pd.DataFrame([features], columns=self.feature_names)
        
        # CRITICAL FIX: Ensure the DataFrame has the exact column names the model expects
        # Rename 'gender_male' to 'gender_Male' if needed
        if 'gender_male' in feature_df.columns and 'gender_Male' not in feature_df.columns:
            feature_df = feature_df.rename(columns={'gender_male': 'gender_Male'})
            print(f"✅ Renamed 'gender_male' to 'gender_Male' to match model expectations")
        
        # Check if all expected columns are present
        expected_columns = ['gender_Male', 'gender_Other']
        for col in expected_columns:
            if col not in feature_df.columns:
                print(f"⚠️ Warning: Expected column '{col}' is missing")
        
        print(f"🔧 DataFrame created: {feature_df.shape} with columns: {feature_df.columns.tolist()}")
        
        return feature_df
    
    def validate_features(self, features: List[float]) -> bool:
        """Validate that features are correct."""
        
        if not isinstance(features, list):
            print(f"❌ Features should be a list, got {type(features)}")
            return False
        
        if len(features) != len(self.feature_names):
            print(f"❌ Wrong number of features: {len(features)} vs {len(self.feature_names)}")
            return False
        
        # Check for NaN or inf values
        for i, f in enumerate(features):
            if isinstance(f, (int, float)):
                if np.isnan(f) or np.isinf(f):
                    print(f"❌ Feature {i} ({self.feature_names[i]}) contains NaN or inf value: {f}")
                    return False
            elif isinstance(f, bool):
                pass  # Booleans are fine
            else:
                print(f"❌ Feature {i} ({self.feature_names[i]}) has unexpected type: {type(f)}")
                return False
        
        print(f"✅ Features validation passed: {len(features)} features")
        return True
    
    def get_feature_descriptions(self) -> Dict[str, str]:
        """Get human-readable descriptions of all features."""
        
        descriptions = {
            'age': 'Patient age in years',
            'hypertension': 'Has hypertension (1=yes, 0=no)',
            'heart_disease': 'Has heart disease (1=yes, 0=no)',
            'avg_glucose_level': 'Average glucose level (mg/dL)',
            'bmi': 'Body Mass Index',
            'gender_male': 'Is male (1=yes, 0=no)',
            'gender_female': 'Is female (1=yes, 0=no)',
            'married': 'Is married (1=yes, 0=no)',
            'age_decade': 'Age divided by 10',
            'age_high_risk': 'Is elderly (age >= 65)',
            'cv_risk_count': 'Count of cardiovascular risk factors',
            'hypertension_elderly': 'Has hypertension AND is elderly',
            'female_elderly': 'Is female AND elderly',
            'male_age_interaction': 'Male gender × age interaction',
            'age_hypertension': 'Age × hypertension interaction',
            'bmi_hypertension': 'BMI × hypertension interaction',
            'glucose_heart_disease': 'Glucose × heart disease interaction',
            'age_hypertension_diabetes': 'Age × hypertension × diabetes interaction',
            'bmi_glucose': 'BMI × glucose interaction',
            'age_obesity': 'Age × obesity interaction',
            'bmi_diabetes': 'BMI × diabetes interaction',
            'age_diabetes': 'Age × diabetes interaction',
            'modifiable_risk_count': 'Count of modifiable risk factors',
            'work_stress_level': 'Work stress level (default: 2)',
            'high_stress_work': 'Has high stress work (default: 0)',
            'gender_Male': 'Is male (1=yes, 0=no)',
            'gender_Other': 'Is other gender (1=yes, 0=no, default: 0)'
        }
        
        return descriptions
    
    def debug_feature_creation(self, patient_data: Dict) -> None:
        """Debug feature creation process with detailed output."""
        
        print(f"\n🔍 DEBUGGING FEATURE CREATION")
        print("-" * 40)
        
        print(f"📥 Input patient data:")
        for key, value in patient_data.items():
            print(f"   {key}: {value}")
        
        # Create features
        features = self.engineer_features(patient_data)
        
        # Show non-zero features
        print(f"\n🔧 Created Features (non-zero only):")
        for i, (name, value) in enumerate(zip(self.feature_names, features)):
            if value != 0:
                print(f"   {i:2d}. {name:25s}: {value}")
        
        # Show feature statistics
        print(f"\n📊 Feature Statistics:")
        print(f"   Total features: {len(features)}")
        print(f"   Non-zero features: {sum(1 for f in features if f != 0)}")
        print(f"   Min value: {min(features):.3f}")
        print(f"   Max value: {max(features):.3f}")
        print(f"   Mean value: {np.mean(features):.3f}")
        
        # Validate
        is_valid = self.validate_features(features)
        print(f"   Validation: {'✅ PASSED' if is_valid else '❌ FAILED'}")

# Backward compatibility: alias the old name to the new class
# This allows existing code to still work
FeatureEngineer = FixedFeatureEngineer

# Test function
def test_feature_engineer():
    """Test the feature engineer with various patient types."""
    
    print("🧪 TESTING FEATURE ENGINEER")
    print("=" * 40)
    
    # Create feature engineer
    fe = FixedFeatureEngineer()
    
    # Test cases
    test_cases = [
        {
            'name': 'High Risk Patient',
            'data': {
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
        },
        {
            'name': 'Low Risk Patient',
            'data': {
                'age': 25.0,
                'gender': 'Female',
                'hypertension': 0,
                'heart_disease': 0,
                'ever_married': 'No',
                'work_type': 'Private',
                'Residence_type': 'Urban',
                'avg_glucose_level': 85.0,
                'bmi': 22.0,
                'smoking_status': 'never_smoked'
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n👤 Testing: {test_case['name']}")
        print("-" * 30)
        
        try:
            # Test list output
            features_list = fe.engineer_features(test_case['data'])
            print(f"✅ List features: {len(features_list)} features created")
            
            # Test DataFrame output
            features_df = fe.create_feature_dataframe(test_case['data'])
            print(f"✅ DataFrame features: {features_df.shape}")
            
            # Validate
            is_valid = fe.validate_features(features_list)
            print(f"✅ Validation: {'PASSED' if is_valid else 'FAILED'}")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # Run tests when script is executed directly
    test_feature_engineer()