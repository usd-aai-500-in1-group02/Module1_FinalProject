import streamlit as st
from typing import Dict, List, Tuple

class InputValidator:
    def __init__(self):
        self.validation_rules = {
            'age': (18, 120),
            'bmi': (10.0, 70.0),
            'avg_glucose_level': (50.0, 400.0)
        }
    
    def validate_patient_data(self, data: Dict) -> Tuple[bool, List[str]]:
        """Validate all patient input data"""
        errors = []
        
        # Range validations
        for field, (min_val, max_val) in self.validation_rules.items():
            if field in data:
                if not (min_val <= data[field] <= max_val):
                    errors.append(f"{field} must be between {min_val} and {max_val}")
        
        # Clinical reasonableness checks
        if data.get('age', 0) < 18:
            errors.append("Age must be 18 or older")
        
        if data.get('bmi', 0) < 12 and data.get('age', 0) > 18:
            errors.append("BMI seems unrealistically low for an adult")
        
        # Glucose level warnings
        if data.get('avg_glucose_level', 0) > 300:
            st.warning("⚠️ Extremely high glucose level detected. Please verify this value.")
        
        return len(errors) == 0, errors
    
    def display_validation_errors(self, errors: List[str]):
        """Display validation errors in Streamlit"""
        if errors:
            st.error("Please correct the following issues:")
            for error in errors:
                st.error(f"• {error}")