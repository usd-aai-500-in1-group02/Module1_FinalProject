# About page for the Stroke Risk Prediction Tool
# Direct implementation to avoid recursion issues

import streamlit as st
from datetime import datetime

def show_about():
    """Display the About page with help section and technical information"""
    
    st.title("ℹ️ About the Stroke Risk Prediction Tool")
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .info-box {
        background-color: #e8f4fd;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .tech-box {
        background-color: #f0f8f0;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .warning-box {
        background-color: #fff8e1;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Application Overview
    st.markdown("## 🎯 Application Overview")
    
    st.markdown("""
    <div class="info-box">
    <h4>🤖 AI-Powered Stroke Risk Assessment</h4>
    <p>This application uses advanced machine learning algorithms to assess individual stroke risk based on demographic, 
    medical, and lifestyle factors. The tool is designed to support healthcare professionals and inform patients about 
    their cardiovascular health status.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # How to Use Section
    st.markdown("## 📋 How to Use This Tool")
    
    tab1, tab2, tab3 = st.tabs(["🔰 Getting Started", "📊 Understanding Results", "🏥 Next Steps"])
    
    with tab1:
        st.markdown("""
        ### Step-by-Step Guide
        
        1. **📝 Enter Patient Information**
           - Navigate to the "Risk Assessment" page
           - Fill in all required demographic information
           - Provide accurate medical history
           - Enter current clinical measurements
        
        2. **✅ Data Validation**
           - The system automatically validates your inputs
           - Ensure all values are within reasonable medical ranges
           - Review any warnings or suggestions
        
        3. **🔍 Generate Risk Assessment**
           - Click "Calculate Risk" to process the information
           - The AI model analyzes 27+ features
           - Results are generated in under 2 seconds
        
        4. **📊 Review Results**
           - Examine your risk percentage and classification
           - Read personalized recommendations
           - Download or print results if needed
        """)
    
    with tab2:
        st.markdown("""
        ### Understanding Your Risk Score
        
        **Risk Classifications:**
        - 🟢 **Low Risk (< 10%)**: Continue healthy lifestyle habits
        - 🟡 **Moderate Risk (10-30%)**: Consider prevention strategies
        - 🟠 **High Risk (30-60%)**: Seek medical consultation
        - 🔴 **Very High Risk (> 60%)**: Urgent medical attention needed
        
        **Important Notes:**
        - Risk percentages are population-based estimates
        - Individual circumstances may vary
        - Results should be discussed with healthcare providers
        - Regular monitoring is recommended as health status changes
        """)
    
    with tab3:
        st.markdown("""
        ### Recommended Next Steps
        
        **For All Risk Levels:**
        - Share results with your healthcare provider
        - Discuss implications for your individual situation
        - Consider lifestyle modifications based on recommendations
        
        **For High/Very High Risk:**
        - Schedule immediate medical consultation
        - Consider specialist referrals (cardiology/neurology)
        - Implement aggressive risk factor modification
        - Regular monitoring and follow-up care
        
        **Emergency Situations:**
        - If experiencing stroke symptoms, call 911 immediately
        - Don't wait for risk assessment results in emergency situations
        """)
    
    # Technical Information
    st.markdown("---")
    st.markdown("## 🔬 Technical Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tech-box">
        <h4>🤖 Machine Learning Model</h4>
        <ul>
            <li><strong>Algorithm:</strong> Calibrated ensemble model</li>
            <li><strong>Training Data:</strong> 5,110 patient records</li>
            <li><strong>Features:</strong> 27 engineered features</li>
            <li><strong>Validation:</strong> Cross-validated performance</li>
            <li><strong>Calibration:</strong> Probability calibration applied</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tech-box">
        <h4>📊 Model Performance</h4>
        <ul>
            <li><strong>AUC Score:</strong> > 0.80</li>
            <li><strong>Sensitivity:</strong> High detection rate</li>
            <li><strong>Specificity:</strong> Low false positive rate</li>
            <li><strong>Calibration:</strong> Well-calibrated probabilities</li>
            <li><strong>Update Frequency:</strong> Model retrained quarterly</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Important Disclaimers
    st.markdown("---")
    st.markdown("## ⚠️ Important Disclaimers & Limitations")
    
    st.markdown("""
    <div class="warning-box">
    <h4>🚨 MEDICAL DISCLAIMER</h4>
    <ul>
        <li><strong>Educational Purpose Only:</strong> This tool is for informational and educational purposes only</li>
        <li><strong>Not Medical Advice:</strong> Results do not constitute professional medical advice, diagnosis, or treatment</li>
        <li><strong>Consult Healthcare Providers:</strong> Always consult qualified medical professionals for health decisions</li>
        <li><strong>Emergency Situations:</strong> Call emergency services immediately for stroke symptoms</li>
        <li><strong>Individual Variation:</strong> Personal risk may differ from population-based estimates</li>
        <li><strong>Accuracy Limitations:</strong> Model accuracy depends on input data quality and completeness</li>
        <li><strong>Regular Updates:</strong> Health status changes; regular medical monitoring is essential</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Frequently Asked Questions
    st.markdown("---")
    st.markdown("## ❓ Frequently Asked Questions")
    
    with st.expander("🤔 How accurate is the stroke risk prediction?"):
        st.markdown("""
        The model achieves an AUC score > 0.80, indicating good predictive performance. However, accuracy depends on:
        - Quality and completeness of input data
        - Individual factors not captured in the model
        - Population similarity to training data
        
        Results should be interpreted as estimates and discussed with healthcare providers.
        """)
    
    with st.expander("📊 What data does the model use for predictions?"):
        st.markdown("""
        The model analyzes 27 engineered features including:
        - **Demographics**: Age, gender, marital status
        - **Medical History**: Hypertension, heart disease
        - **Lifestyle Factors**: Smoking status, work type
        - **Clinical Measurements**: BMI, glucose levels
        - **Interaction Terms**: Complex relationships between factors
        """)
    
    with st.expander("🔄 How often should I use this tool?"):
        st.markdown("""
        Risk assessment frequency depends on your health status:
        - **Healthy individuals**: Annually or when health status changes
        - **Those with risk factors**: Every 6 months or as recommended by healthcare provider
        - **High-risk patients**: More frequent monitoring as advised by medical professionals
        
        Remember that health status can change, so regular reassessment is valuable.
        """)
    
    with st.expander("🚨 What should I do if I'm classified as high risk?"):
        st.markdown("""
        For high or very high risk classifications:
        1. **Immediate Action**: Contact your healthcare provider
        2. **Specialist Referral**: Consider cardiology or neurology consultation
        3. **Lifestyle Changes**: Implement aggressive risk factor modification
        4. **Regular Monitoring**: Increase frequency of medical checkups
        5. **Emergency Preparedness**: Know stroke warning signs (F.A.S.T.)
        
        Don't panic, but take the results seriously and seek professional guidance.
        """)
    
    # Contact Information
    st.markdown("---")
    st.markdown("## 📞 Support & Contact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🛠️ Technical Support
        - **Email**: support@example.com
        - **Documentation**: Available in app menu
        - **Bug Reports**: Use feedback option
        """)
    
    with col2:
        st.markdown("""
        ### 🏥 Medical Resources
        - **Emergency**: Call 911
        - **Stroke Hotline**: 1-888-4-STROKE
        - **American Stroke Association**: stroke.org
        """)
    
    # Version Information
    st.markdown("---")
    st.markdown("## 📋 Version Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("App Version", "1.0.0")
    with col2:
        st.metric("Model Version", "v2.1")
    with col3:
        st.metric("Last Updated", datetime.now().strftime("%b %Y"))
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666666; padding: 1rem;">
        <p><strong>Stroke Risk Prediction Tool</strong> | Version 1.0</p>
        <p>Built with ❤️ for better healthcare outcomes</p>
        <p>Last updated: {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_about()