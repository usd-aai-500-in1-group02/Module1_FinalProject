# Updated pages/risk_assessment.py with proper session state management
import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

try:
    from model_handler import ModelHandler
    from input_validation import InputValidator
    from feature_engineering import FeatureEngineer
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Make sure all required modules are in the src directory")

# Page configuration
st.set_page_config(
    page_title="Risk Assessment",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2e8b57;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #2e8b57;
        padding-bottom: 0.5rem;
    }
    .input-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .prediction-button {
        background: linear-gradient(45deg, #1f77b4, #2e8b57);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        margin: 1rem 0;
    }
    .risk-summary {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the stroke prediction model."""
    try:
        model_handler = ModelHandler()
        st.session_state.model_loaded = True
        return model_handler
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        st.session_state.model_loaded = False
        return None

@st.cache_resource
def load_validator():
    """Load the input validator."""
    return InputValidator()

def main():
    """Main risk assessment page."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Stroke Risk Assessment</h1>', unsafe_allow_html=True)
    
    # Load model and validator
    model_handler = load_model()
    if not model_handler:
        st.error("❌ Model loading failed. Please check your model files.")
        return
    
    validator = load_validator()
    
    # Create form for patient input
    with st.form("patient_assessment_form"):
        st.markdown('<div class="section-header">👤 Patient Information</div>', unsafe_allow_html=True)
        
        # Basic demographics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input(
                "Age (years)",
                min_value=18,
                max_value=100,
                value=50,
                step=1,
                help="Patient's age in years"
            )
        
        with col2:
            gender = st.selectbox(
                "Gender",
                options=["Male", "Female"],
                help="Biological gender"
            )
        
        with col3:
            marital_status = st.selectbox(
                "Marital Status",
                options=["Married", "Single", "Divorced", "Widowed"],
                help="Current marital status"
            )
        
        st.markdown('<div class="section-header">🏥 Medical Measurements</div>', unsafe_allow_html=True)
        
        # Medical measurements
        col1, col2 = st.columns(2)
        
        with col1:
            bmi = st.number_input(
                "BMI (Body Mass Index)",
                min_value=10.0,
                max_value=50.0,
                value=25.0,
                step=0.1,
                format="%.1f",
                help="Weight (kg) / Height (m)²"
            )
            
            # BMI category indicator is now removed as requested
        
        with col2:
            glucose_level = st.number_input(
                "Average Glucose Level (mg/dL)",
                min_value=50,
                max_value=400,
                value=100,
                step=1,
                help="Average blood glucose level"
            )
            
            # Glucose category indicator is now removed as requested
        
        st.markdown('<div class="section-header">🩺 Medical Conditions</div>', unsafe_allow_html=True)
        
        # Medical conditions
        col1, col2 = st.columns(2)
        
        with col1:
            hypertension = st.selectbox(
                "Hypertension (High Blood Pressure)",
                options=["No", "Yes"],
                help="History of hypertension"
            )
        
        with col2:
            heart_disease = st.selectbox(
                "Heart Disease",
                options=["No", "Yes"],
                help="History of heart disease"
            )
        
        st.markdown('<div class="section-header">🚬 Lifestyle Factors</div>', unsafe_allow_html=True)
        
        # Lifestyle factors
        col1, col2 = st.columns(2)
        
        with col1:
            smoking_status = st.selectbox(
                "Smoking Status",
                options=["Never smoked", "Formerly smoked", "Currently smokes", "Unknown"],
                help="Current smoking status"
            )
        
        with col2:
            work_type = st.selectbox(
                "Work Type",
                options=["Private", "Self-employed", "Government", "Retired", "Student"],
                help="Type of work or employment status"
            )
        
        # Additional information
        residence_type = st.selectbox(
            "Residence Type",
            options=["Urban", "Rural"],
            help="Type of residential area"
        )
        
        # Form submission
        st.markdown("---")
        
        # CRITICAL FIX 2: Updated prediction button with session state storage
        submitted = st.form_submit_button(
            "🔮 Analyze Stroke Risk",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Basic input validation first
            if age < 18 or age > 100:
                st.error("❌ Please enter a valid age between 18 and 100")
                return
            
            if bmi < 10 or bmi > 50:
                st.error("❌ Please enter a valid BMI between 10 and 50")
                return
            
            if glucose_level < 50 or glucose_level > 400:
                st.error("❌ Please enter a valid glucose level between 50 and 400")
                return
            
            # Prepare patient data for ModelHandler
            patient_data = {
                'age': float(age),
                'gender': gender,
                'hypertension': 1 if hypertension == "Yes" else 0,
                'heart_disease': 1 if heart_disease == "Yes" else 0,
                'ever_married': "Yes" if marital_status == "Married" else "No",
                'work_type': work_type,
                'Residence_type': residence_type,
                'avg_glucose_level': float(glucose_level),
                'bmi': float(bmi),
                'smoking_status': smoking_status.lower().replace(' ', '_')
            }
            
            # Validate inputs using InputValidator
            is_valid, validation_errors = validator.validate_patient_data(patient_data)
            
            if not is_valid:
                validator.display_validation_errors(validation_errors)
                return
            
            # Also validate with ModelHandler's validation
            model_valid, model_errors = model_handler.validate_prediction_inputs(patient_data)
            
            if not model_valid:
                st.error("❌ Model validation failed:")
                for error in model_errors:
                    st.error(f"• {error}")
                return
            
            # Show processing
            with st.spinner("🔄 Analyzing risk factors... Please wait"):
                try:
                    # Make prediction using ModelHandler
                    probability, risk_level, feature_importance = model_handler.predict_stroke_risk(patient_data)
                    
                    # Convert to percentage and create results dict
                    probability_percent = probability * 100
                    
                    results = {
                        'probability': probability,
                        'probability_percent': probability_percent,
                        'risk_level': risk_level,
                        'feature_importance': feature_importance,
                        'success': True
                    }
                    
                    # 🔥 CRITICAL FIX: Store results in session state
                    st.session_state.prediction_results = results
                    st.session_state.patient_data = patient_data
                    
                    # DEBUG: Show what was stored
                    if st.checkbox("🔧 Show stored data (debug)"):
                        st.write("**Stored Results:**")
                        st.json(results)
                        st.write("**Stored Patient Data:**")
                        st.json(patient_data)
                    
                    # Show success message
                    st.success("✅ Risk assessment completed successfully!")
                    
                    # Show quick preview
                    # Risk level colors
                    risk_colors = {
                        'Low Risk': '#28a745',
                        'Moderate Risk': '#ffc107', 
                        'High Risk': '#fd7e14',
                        'Very High Risk': '#dc3545'
                    }
                    
                    risk_emojis = {
                        'Low Risk': '🟢',
                        'Moderate Risk': '🟡',
                        'High Risk': '🟠', 
                        'Very High Risk': '🔴'
                    }
                    
                    color = risk_colors.get(risk_level, '#6c757d')
                    emoji = risk_emojis.get(risk_level, '⚪')
                    
                    st.markdown(f"""
                    <div class="risk-summary">
                        <h3 style="color: {color}; margin: 0;">
                            {emoji} Stroke Risk: {probability_percent:.1f}% ({risk_level})
                        </h3>
                        <p style="margin: 0.5rem 0 0 0;">
                            Risk assessment completed successfully! Navigate to results page to see detailed analysis.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"❌ An error occurred during prediction: {str(e)}")
                    st.error("Please check your model files and try again.")
    
    # Navigation button OUTSIDE the form (this fixes the st.button() error)
    if st.session_state.prediction_results:
        st.markdown("---")
        st.success("✅ Risk assessment completed!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📈 View Detailed Results", use_container_width=True, type="primary"):
                st.switch_page("pages/results.py")
        
        with col2:
            if st.button("🔄 New Assessment", use_container_width=True):
                # Clear session state for new assessment
                st.session_state.prediction_results = None
                st.session_state.patient_data = None
                st.rerun()
    
    # Show current session status
    if st.session_state.prediction_results:
        st.markdown("---")
        st.info("ℹ️ A previous risk assessment is available. Use the navigation menu to view results.")
    
    # Educational information
    with st.expander("📚 Understanding Stroke Risk Factors"):
        st.markdown("""
        ### Major Risk Factors for Stroke:
        
        **🔴 Non-Modifiable Factors:**
        - **Age**: Risk increases significantly after age 65
        - **Gender**: Men have slightly higher risk, but women have more fatal strokes
        - **Genetics**: Family history of stroke increases risk
        
        **🟡 Modifiable Factors:**
        - **Hypertension**: Most important modifiable risk factor
        - **Diabetes**: Doubles stroke risk
        - **Heart Disease**: Atrial fibrillation increases risk 5x
        - **Smoking**: Doubles stroke risk
        - **High Cholesterol**: Contributes to arterial blockage
        - **Obesity**: BMI >30 significantly increases risk
        
        **🟢 Protective Factors:**
        - Regular physical activity
        - Healthy diet (Mediterranean style)
        - Moderate alcohol consumption
        - Social engagement and marriage
        - Good blood pressure control
        """)
    
    with st.expander("🧮 How the Assessment Works"):
        st.markdown("""
        ### Machine Learning Model:
        
        Our stroke risk assessment uses a **Naive Bayes classifier** trained on real medical data:
        
        - **Training Data**: 5,110 patient records
        - **Features**: 27 engineered risk factors
        - **Accuracy**: 85.4% (AUC score)
        - **Validation**: Cross-validated on independent data
        
        ### Feature Engineering:
        
        The model analyzes interactions between risk factors:
        - Age × Gender interactions
        - BMI × Glucose level combinations  
        - Cardiovascular risk clustering
        - Lifestyle factor weighting
        
        ### Risk Categories:
        - **Low Risk**: <5% probability
        - **Medium Risk**: 5-15% probability
        - **High Risk**: 15-30% probability
        - **Very High Risk**: >30% probability
        """)

if __name__ == "__main__":
    main()