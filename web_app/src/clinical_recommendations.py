from typing import Dict, List
import streamlit as st

class ClinicalRecommendations:
    def __init__(self):
        self.recommendations = {
            "Low Risk": {
                "title": "🟢 Low Risk",
                "color": "green",
                "actions": [
                    "Continue healthy lifestyle habits",
                    "Regular health checkups every 1-2 years",
                    "Maintain healthy weight and exercise regularly",
                    "Monitor blood pressure annually"
                ]
            },
            "Moderate Risk": {
                "title": "🟡 Moderate Risk",
                "color": "orange",
                "actions": [
                    "Consult with primary care physician",
                    "Enhanced lifestyle modifications",
                    "Blood pressure monitoring every 6 months",
                    "Consider cardiovascular risk assessment"
                ]
            },
            "High Risk": {
                "title": "🟠 High Risk",
                "color": "red",
                "actions": [
                    "Immediate consultation with healthcare provider",
                    "Comprehensive cardiovascular evaluation",
                    "Consider cardiology referral",
                    "Aggressive risk factor modification"
                ]
            },
            "Very High Risk": {
                "title": "🔴 Very High Risk",
                "color": "darkred",
                "actions": [
                    "URGENT: Contact healthcare provider immediately",
                    "Emergency department evaluation if symptomatic",
                    "Immediate cardiology/neurology referral",
                    "Intensive medical management required"
                ]
            }
        }
    
    def get_recommendations(self, risk_level: str, patient_data: Dict) -> Dict:
        """Generate personalized clinical recommendations"""
        base_recommendations = self.recommendations[risk_level]
        
        # Add personalized recommendations based on modifiable risk factors
        personalized = self._get_personalized_recommendations(patient_data)
        
        return {
            **base_recommendations,
            "personalized": personalized
        }
    
    def _get_personalized_recommendations(self, patient_data: Dict) -> List[str]:
        """Generate personalized recommendations based on patient profile"""
        recommendations = []
        
        if patient_data.get('bmi', 0) > 30:
            recommendations.append("🎯 Weight management: Target BMI < 25")
        
        if patient_data.get('avg_glucose_level', 0) > 140:
            recommendations.append("🍎 Diabetes management: Target glucose < 140 mg/dL")
        
        if patient_data.get('smoking_status') == 'smokes':
            recommendations.append("🚭 Smoking cessation: Immediate priority")
        
        if patient_data.get('hypertension') == 1:
            recommendations.append("💊 Blood pressure control: Target < 130/80 mmHg")
        
        return recommendations