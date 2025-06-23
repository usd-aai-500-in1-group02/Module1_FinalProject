import streamlit as st
from typing import Dict, Any

def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Stroke Risk Prediction",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.streamlit.io',
            'Report a bug': "mailto:support@example.com",
            'About': "# Stroke Risk Prediction Tool\nAI-powered clinical decision support for stroke risk assessment."
        }
    )

def display_header():
    """Display the main application header"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Stroke Risk Prediction Tool</h1>
        <p>AI-Powered Clinical Decision Support System</p>
    </div>
    """, unsafe_allow_html=True)

def create_patient_form() -> Dict[str, Any]:
    """Create and return patient data input form"""
    st.subheader("📋 Patient Information")
    
    # Initialize patient data dictionary
    patient_data = {}
    
    # Demographics Section
    with st.expander("👤 Demographics", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_data['age'] = st.number_input(
                "Age (years)",
                min_value=18,
                max_value=120,
                value=50,
                help="Patient's age in years"
            )
            
            patient_data['gender'] = st.selectbox(
                "Gender",
                options=["Male", "Female"],
                help="Biological gender"
            )
        
        with col2:
            patient_data['ever_married'] = st.selectbox(
                "Marital Status",
                options=["Yes", "No"],
                help="Has the patient ever been married?"
            )
            
            patient_data['Residence_type'] = st.selectbox(
                "Residence Type",
                options=["Urban", "Rural"],
                help="Type of residential area"
            )
    
    # Medical History Section
    with st.expander("🏥 Medical History", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_data['hypertension'] = st.selectbox(
                "Hypertension",
                options=[0, 1],
                format_func=lambda x: "No" if x == 0 else "Yes",
                help="Does the patient have hypertension?"
            )
        
        with col2:
            patient_data['heart_disease'] = st.selectbox(
                "Heart Disease",
                options=[0, 1],
                format_func=lambda x: "No" if x == 0 else "Yes",
                help="Does the patient have heart disease?"
            )
    
    # Work and Lifestyle Section
    with st.expander("💼 Work & Lifestyle", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_data['work_type'] = st.selectbox(
                "Work Type",
                options=["Private", "Self-employed", "Never_worked", "children"],
                help="Patient's employment type"
            )
        
        with col2:
            patient_data['smoking_status'] = st.selectbox(
                "Smoking Status",
                options=["never smoked", "formerly smoked", "smokes", "Unknown"],
                help="Patient's smoking history"
            )
    
    # Clinical Measurements Section
    with st.expander("📊 Clinical Measurements", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_data['bmi'] = st.number_input(
                "BMI (Body Mass Index)",
                min_value=10.0,
                max_value=70.0,
                value=25.0,
                step=0.1,
                format="%.1f",
                help="Body Mass Index (weight in kg / height in m²)"
            )
            
            # BMI interpretation
            bmi_val = patient_data['bmi']
            if bmi_val < 18.5:
                st.info("BMI Category: Underweight")
            elif bmi_val < 25:
                st.success("BMI Category: Normal weight")
            elif bmi_val < 30:
                st.warning("BMI Category: Overweight")
            else:
                st.error("BMI Category: Obese")
        
        with col2:
            patient_data['avg_glucose_level'] = st.number_input(
                "Average Glucose Level (mg/dL)",
                min_value=50.0,
                max_value=400.0,
                value=100.0,
                step=1.0,
                format="%.1f",
                help="Average blood glucose level in mg/dL"
            )
            
            # Glucose interpretation
            glucose_val = patient_data['avg_glucose_level']
            if glucose_val < 100:
                st.success("Glucose Level: Normal")
            elif glucose_val < 126:
                st.warning("Glucose Level: Prediabetic range")
            else:
                st.error("Glucose Level: Diabetic range")
    
    return patient_data

def display_risk_gauge(probability: float, risk_level: str):
    """Display risk gauge using Plotly"""
    import plotly.graph_objects as go
    
    # Determine gauge color based on risk level
    color_map = {
        "Low Risk": "green",
        "Moderate Risk": "yellow", 
        "High Risk": "orange",
        "Very High Risk": "red"
    }
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Stroke Risk: {risk_level}"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color_map.get(risk_level, "blue")},
            'steps': [
                {'range': [0, 10], 'color': "lightgreen"},
                {'range': [10, 30], 'color': "yellow"},
                {'range': [30, 60], 'color': "orange"},
                {'range': [60, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def display_risk_summary(probability: float, risk_level: str, patient_data: Dict):
    """Display risk summary with key information"""
    
    # Risk level color mapping
    color_map = {
        "Low Risk": "🟢",
        "Moderate Risk": "🟡", 
        "High Risk": "🟠",
        "Very High Risk": "🔴"
    }
    
    st.markdown("### 📊 Risk Assessment Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Risk Probability",
            value=f"{probability*100:.1f}%",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Risk Classification",
            value=f"{color_map.get(risk_level, '⚪')} {risk_level}",
            delta=None
        )
    
    with col3:
        # Calculate risk factors count
        risk_factors = sum([
            patient_data.get('hypertension', 0),
            patient_data.get('heart_disease', 0),
            1 if patient_data.get('bmi', 0) > 30 else 0,
            1 if patient_data.get('avg_glucose_level', 0) > 140 else 0,
            1 if patient_data.get('smoking_status') == 'smokes' else 0
        ])
        
        st.metric(
            label="Risk Factors Present",
            value=f"{risk_factors}/5",
            delta=None
        )

def create_sidebar_navigation():
    """Create sidebar navigation"""
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("📊 Risk Assessment", use_container_width=True):
            st.session_state.page = 'assessment'
            st.rerun()
        
        if st.button("📋 Results", use_container_width=True):
            if 'patient_data' in st.session_state:
                st.session_state.page = 'results'
                st.rerun()
            else:
                st.warning("Please complete assessment first")
        
        if st.button("ℹ️ About", use_container_width=True):
            st.session_state.page = 'about'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🚨 Emergency")
        st.error("**If experiencing stroke symptoms:**\n\nCall 911 immediately!")
        
        st.markdown("---")
        st.markdown("### ℹ️ App Info")
        st.info("Version 1.0\nFor educational use only")

def show_loading_spinner(text="Processing..."):
    """Show loading spinner with custom text"""
    with st.spinner(text):
        import time
        time.sleep(1)  # Simulate processing time