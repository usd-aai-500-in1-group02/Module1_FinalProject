import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

def show_home():
    """Display the home/landing page with app introduction and disclaimers"""
    
    # Page configuration
    st.set_page_config(
        page_title="Stroke Risk Prediction",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: #1f4e79;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666666;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .disclaimer-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .stats-box {
        background-color: #e7f3ff;
        border: 1px solid #007bff;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        🏥 Stroke Risk Prediction Tool
    </div>
    <div class="sub-header">
        AI-Powered Clinical Decision Support for Stroke Risk Assessment
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section with key stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-box">
            <h3>🧠 About Stroke</h3>
            <p><strong>2nd</strong> leading cause of death globally</p>
            <p><strong>795,000</strong> strokes occur in the US annually</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-box">
            <h3>⏱️ Time Critical</h3>
            <p><strong>Every minute</strong> counts in stroke prevention</p>
            <p><strong>Early detection</strong> saves lives</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-box">
            <h3>🎯 Prevention</h3>
            <p><strong>80%</strong> of strokes are preventable</p>
            <p><strong>Risk assessment</strong> enables prevention</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # App introduction
    st.markdown("## 🎯 What is This Tool?")
    
    st.markdown("""
    <div class="feature-box">
    <h4>🤖 AI-Powered Risk Assessment</h4>
    <p>Our tool uses advanced machine learning algorithms trained on comprehensive medical data to assess individual stroke risk. 
    The model analyzes multiple risk factors including demographics, medical history, and clinical measurements to provide 
    personalized risk predictions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key features
    st.markdown("## ✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔍 Comprehensive Analysis
        - **Demographics**: Age, gender, lifestyle factors
        - **Medical History**: Hypertension, heart disease
        - **Clinical Measurements**: BMI, glucose levels
        - **Lifestyle Factors**: Smoking status, work type
        """)
        
        st.markdown("""
        ### 📊 Evidence-Based Results
        - **4-Tier Risk Classification**: Low, Moderate, High, Very High
        - **Percentage Risk Score**: Clear numerical probability
        - **Visual Risk Gauge**: Easy-to-understand graphics
        - **Feature Importance**: Key contributing factors
        """)
    
    with col2:
        st.markdown("""
        ### 🏥 Clinical Recommendations
        - **Personalized Guidance**: Tailored to individual risk profile
        - **Actionable Steps**: Specific prevention strategies
        - **Medical Referrals**: When to seek professional care
        - **Lifestyle Modifications**: Evidence-based interventions
        """)
        
        st.markdown("""
        ### ⚡ User-Friendly Interface
        - **Professional Design**: Medical-grade interface
        - **Real-time Validation**: Input error checking
        - **Mobile Responsive**: Works on all devices
        - **Fast Results**: Predictions in under 2 seconds
        """)
    
    # How it works section
    st.markdown("---")
    st.markdown("## 🔄 How It Works")
    
    # Process flow
    process_steps = [
        ("📝 Input Data", "Enter patient demographics and medical information"),
        ("🔍 Data Validation", "System validates inputs for clinical reasonableness"),
        ("🤖 AI Analysis", "Machine learning model processes 28+ features"),
        ("📊 Risk Calculation", "Calibrated probability and risk classification"),
        ("🏥 Recommendations", "Personalized clinical guidance and next steps")
    ]
    
    for i, (title, description) in enumerate(process_steps, 1):
        with st.container():
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                st.markdown(f"""
                <div class="feature-box">
                <h4>Step {i}: {title}</h4>
                <p>{description}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Important disclaimers
    st.markdown("---")
    st.markdown("## ⚠️ Important Medical Disclaimers")
    
    st.markdown("""
    <div class="disclaimer-box">
    <h4>🚨 MEDICAL DISCLAIMER</h4>
    <ul>
        <li><strong>Not a substitute for professional medical advice:</strong> This tool is for informational and educational purposes only.</li>
        <li><strong>Emergency situations:</strong> If you are experiencing stroke symptoms (sudden numbness, confusion, trouble speaking, severe headache), call emergency services immediately.</li>
        <li><strong>Consult healthcare providers:</strong> Always discuss results with qualified medical professionals before making health decisions.</li>
        <li><strong>Individual variation:</strong> Risk predictions are population-based estimates and may not reflect individual circumstances.</li>
        <li><strong>Regular monitoring:</strong> Health status can change; regular medical checkups are essential.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Stroke warning signs
    st.markdown("## 🚨 Know the Warning Signs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### **F.A.S.T. Assessment**
        - **F**ace: Sudden numbness or weakness in face
        - **A**rms: Sudden numbness or weakness in arm
        - **S**peech: Sudden confusion, trouble speaking
        - **T**ime: Call emergency services immediately
        """)
    
    with col2:
        st.markdown("""
        ### **Other Warning Signs**
        - Sudden severe headache
        - Sudden trouble seeing
        - Sudden trouble walking
        - Sudden dizziness or loss of coordination
        """)
    
    # Call to action
    st.markdown("---")
    
    # Center the button using columns
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        if st.button("🔍 Start Risk Assessment", type="primary", use_container_width=True):
            st.session_state.page = 'assessment'
            st.rerun()
    
    # Additional information
    st.markdown("---")
    
    # Footer information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📞 Emergency Numbers
        - **US Emergency**: 911
        - **Stroke Hotline**: 1-888-4-STROKE
        - **Poison Control**: 1-800-222-1222
        """)
    
    with col2:
        st.markdown("""
        ### 🔗 Additional Resources
        - [American Stroke Association](https://www.stroke.org)
        - [CDC Stroke Information](https://www.cdc.gov/stroke)
        - [National Stroke Association](https://www.stroke.org)
        """)
    
    # App information
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666666; font-size: 0.9rem;">
    <p>Stroke Risk Prediction Tool v1.0 | Last Updated: {datetime.now().strftime('%B %Y')}</p>
    <p>For healthcare professionals and informed patients | Educational use only</p>
    </div>
    """, unsafe_allow_html=True)

# Main execution
if __name__ == "__main__":
    show_home()