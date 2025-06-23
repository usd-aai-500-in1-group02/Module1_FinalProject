# Updated pages/results.py with dynamic values and proper session state usage
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Risk Assessment Results",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for results page
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-low {
        border-left-color: #28a745 !important;
        background-color: #d4edda !important;
    }
    .risk-medium {
        border-left-color: #ffc107 !important;
        background-color: #fff3cd !important;
    }
    .risk-high {
        border-left-color: #fd7e14 !important;
        background-color: #ffeaa7 !important;
    }
    .risk-very-high {
        border-left-color: #dc3545 !important;
        background-color: #f8d7da !important;
    }
    .patient-summary {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .recommendation-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: bold;
    }
    .alert-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .alert-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def create_risk_gauge(probability_percent, risk_level):
    """Create dynamic risk gauge meter using actual prediction results."""
    
    # CRITICAL FIX 3: Use dynamic values instead of hardcoded 0.1
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = probability_percent,  # ← DYNAMIC VALUE (was hardcoded 0.1)
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': f"{risk_level} Risk<br><span style='font-size:0.8em'>Stroke Risk Probability</span>",
            'font': {'size': 24}
        },
        delta = {'reference': 4.9, 'valueformat': ".1f"},
        gauge = {
            'axis': {
                'range': [None, 100], 
                'tickwidth': 1, 
                'tickcolor': "darkblue",
                'tickvals': [0, 20, 40, 60, 80, 100],
                'ticktext': ['0%', '20%', '40%', '60%', '80%', '100%']
            },
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': '#d4edda'},      # Low risk
                {'range': [5, 15], 'color': '#fff3cd'},     # Medium risk  
                {'range': [15, 30], 'color': '#ffeaa7'},    # High risk
                {'range': [30, 100], 'color': '#f8d7da'}    # Very high risk
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': probability_percent  # ← DYNAMIC THRESHOLD (was hardcoded)
            }
        },
        number = {
            'suffix': "%",
            'font': {'size': 40, 'color': "darkblue"}
        }
    ))
    
    fig.update_layout(
        height=400,
        font={'color': "darkblue", 'family': "Arial"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def display_patient_summary():
    """Display patient summary using session state data."""
    
    st.markdown('<h2>👤 Patient Summary</h2>', unsafe_allow_html=True)
    
    # CRITICAL FIX 4: Use session state patient data instead of form inputs
    if st.session_state.patient_data:
        patient = st.session_state.patient_data
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            age = patient.get('age', 'Unknown')
            st.metric("Age", f"{age:.0f} years")
        
        with col2:
            gender = patient.get('gender', 'Unknown')
            st.metric("Gender", gender)
        
        with col3:
            bmi = patient.get('bmi', 0)
            if bmi >= 30:
                bmi_status = "↗️ Obese"
            elif bmi >= 25:
                bmi_status = "↗️ Overweight"
            else:
                bmi_status = "✅ Normal"
            st.metric("BMI", f"{bmi:.1f}", delta=bmi_status)
        
        with col4:
            glucose = patient.get('avg_glucose_level', 0)
            if glucose > 125:
                glucose_status = "↗️ Diabetic"
            elif glucose > 100:
                glucose_status = "⚠️ Pre-diabetic"
            else:
                glucose_status = "✅ Normal"
            st.metric("Glucose", f"{glucose:.0f} mg/dL", delta=glucose_status)
    
    else:
        st.error("❌ No patient data found. Please complete the risk assessment first.")

def display_risk_analysis():
    """Display risk analysis using dynamic prediction results."""
    
    st.markdown('<h2>📊 Risk Analysis Summary</h2>', unsafe_allow_html=True)
    
    # CRITICAL FIX 5: Check if prediction results exist
    if not st.session_state.prediction_results:
        st.error("❌ No prediction results found. Please complete the risk assessment first.")
        if st.button("📊 Go to Risk Assessment", use_container_width=True):
            st.switch_page("pages/risk_assessment.py")
        return
    
    # Get results from session state
    results = st.session_state.prediction_results
    patient = st.session_state.patient_data
    
    # DYNAMIC risk values (not hardcoded!)
    probability_percent = results.get('probability_percent', 0)
    risk_level = results.get('risk_level', 'Unknown')
    
    # Risk level styling
    risk_classes = {
        'Low Risk': 'risk-low',
        'Moderate Risk': 'risk-medium',
        'High Risk': 'risk-high',
        'Very High Risk': 'risk-very-high'
    }
    
    risk_emojis = {
        'Low Risk': '🟢',
        'Moderate Risk': '🟡',
        'High Risk': '🟠',
        'Very High Risk': '🔴'
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # CRITICAL FIX 6: Dynamic gauge meter
        fig = create_risk_gauge(probability_percent, risk_level)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # CRITICAL FIX 7: Dynamic risk probability display
        risk_class = risk_classes.get(risk_level, '')
        st.markdown(f"""
        <div class="metric-card {risk_class}">
            <h3>Risk Probability</h3>
            <h1>{probability_percent:.1f}%</h1>
            <p>vs. 4.9% population average</p>
        </div>
        """, unsafe_allow_html=True)
        
        # CRITICAL FIX 8: Dynamic risk classification
        risk_emoji = risk_emojis.get(risk_level, '⚪')
        st.markdown(f"""
        <div class="metric-card {risk_class}">
            <h3>Risk Classification</h3>
            <h2>{risk_emoji} {risk_level} Risk</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # CRITICAL FIX 9: Dynamic modifiable risk factors count
        modifiable_count = 0
        modifiable_factors = []
        
        if patient.get('hypertension', 0):
            modifiable_count += 1
            modifiable_factors.append("Hypertension")
        
        if patient.get('avg_glucose_level', 0) > 125:
            modifiable_count += 1
            modifiable_factors.append("Diabetes")
        
        if patient.get('bmi', 0) >= 30:
            modifiable_count += 1
            modifiable_factors.append("Obesity")
        elif patient.get('bmi', 0) >= 25:
            modifiable_count += 1
            modifiable_factors.append("Overweight")
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Modifiable Risk Factors</h3>
            <h2>{modifiable_count}/3</h2>
            <p>↗️ Focus areas for prevention</p>
        </div>
        """, unsafe_allow_html=True)

def display_risk_factors():
    """Display detailed risk factor analysis."""
    
    st.markdown('<h2>📈 Risk Factor Analysis</h2>', unsafe_allow_html=True)
    
    if not st.session_state.patient_data or not st.session_state.prediction_results:
        st.error("No patient data or prediction results available.")
        return
    
    patient = st.session_state.patient_data
    results = st.session_state.prediction_results
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Present Risk Factors")
        
        risk_factors = []
        
        # Age factor
        age = patient.get('age', 0)
        if age >= 65:
            risk_factors.append(f"• **Advanced age** ({age:.0f} years)")
        
        # Medical conditions
        if patient.get('hypertension', 0):
            risk_factors.append("• **Hypertension** (High blood pressure)")
        
        if patient.get('heart_disease', 0):
            risk_factors.append("• **Heart disease**")
        
        # Metabolic factors
        glucose = patient.get('avg_glucose_level', 0)
        if glucose > 125:
            risk_factors.append(f"• **Diabetes** (Glucose: {glucose:.0f} mg/dL)")
        elif glucose > 100:
            risk_factors.append(f"• **Pre-diabetes** (Glucose: {glucose:.0f} mg/dL)")
        
        # BMI factors
        bmi = patient.get('bmi', 0)
        if bmi >= 30:
            risk_factors.append(f"• **Obesity** (BMI: {bmi:.1f})")
        elif bmi >= 25:
            risk_factors.append(f"• **Overweight** (BMI: {bmi:.1f})")
        
        # Smoking status
        smoking = patient.get('smoking_status', '')
        if 'smokes' in smoking or smoking == 'currently_smokes':
            risk_factors.append("• **Current smoking**")
        elif 'formerly' in smoking or smoking == 'formerly_smoked':
            risk_factors.append("• **Former smoking history**")
        
        if risk_factors:
            for factor in risk_factors:
                st.markdown(factor)
        else:
            st.success("✅ No major risk factors identified")
    
    with col2:
        st.subheader("Risk Level Comparison")
        
        # Population comparison chart
        categories = ['Low<br>(0-5%)', 'Medium<br>(5-15%)', 'High<br>(15-30%)', 'Very High<br>(30%+)']
        population_pct = [70, 20, 8, 2]
        
        # Determine where current patient falls
        prob = results.get('probability_percent', 0)
        risk_level = results.get('risk_level', 'Unknown')  # ← FIX: Get risk_level from results
        patient_data = [0, 0, 0, 0]
        if 'Low' in risk_level:
            patient_data[0] = 100
        elif 'Moderate' in risk_level:
            patient_data[1] = 100
        elif 'High Risk' in risk_level:  # Not "Very High"
            patient_data[2] = 100
        elif 'Very High' in risk_level:
            patient_data[3] = 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Population Average (%)',
            x=categories,
            y=population_pct,
            marker_color='lightblue',
            opacity=0.7,
            text=population_pct,
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            name='Current Patient',
            x=categories,
            y=patient_data,
            marker_color='red',
            opacity=0.8,
            text=['You' if x > 0 else '' for x in patient_data],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Population Risk Distribution",
            xaxis_title="Risk Category",
            yaxis_title="Percentage",
            barmode='overlay',
            height=350,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_recommendations():
    """Display personalized recommendations based on patient data."""
    
    st.markdown('<h2>💡 Personalized Recommendations</h2>', unsafe_allow_html=True)
    
    if not st.session_state.patient_data:
        st.error("No patient data available for recommendations.")
        return
    
    patient = st.session_state.patient_data
    results = st.session_state.prediction_results
    
    # Risk-based alert
    risk_level = results.get('risk_level', 'Unknown')
    probability = results.get('probability_percent', 0)
    
    if 'Very High' in risk_level:
        alert_class = "alert-danger"
        alert_icon = "🚨"
        alert_text = "Very High Risk - Immediate medical consultation recommended"
    elif 'High' in risk_level:
        alert_class = "alert-warning"
        alert_icon = "⚠️"
        alert_text = "High Risk - Comprehensive evaluation and prevention plan needed"
    elif 'Moderate' in risk_level:
        alert_class = "alert-warning"
        alert_icon = "⚠️"
        alert_text = "Moderate Risk - Preventive measures and lifestyle changes recommended"
    else:
        alert_class = "alert-success"
        alert_icon = "✅"
        alert_text = "Low Risk - Continue healthy lifestyle practices"
    
    st.markdown(f"""
    <div class="{alert_class}">
        {alert_icon} {alert_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Specific recommendations
    recommendations = []
    
    # Age-based recommendations
    if patient.get('age', 0) >= 65:
        recommendations.append({
            'category': 'Age-Related Care',
            'items': [
                "Regular cardiovascular screening and monitoring",
                "Annual stroke risk assessment",
                "Coordination with geriatric care specialists"
            ]
        })
    
    # Condition-based recommendations
    medical_recs = []
    if patient.get('hypertension', 0):
        medical_recs.extend([
            "Blood pressure monitoring and management",
            "Antihypertensive medication review with physician",
            "Dietary sodium reduction (<2300mg/day)"
        ])
    
    if patient.get('heart_disease', 0):
        medical_recs.extend([
            "Cardiology consultation for comprehensive care",
            "Cardiac risk factor optimization",
            "Regular EKG and echocardiogram monitoring"
        ])
    
    if medical_recs:
        recommendations.append({
            'category': 'Medical Management',
            'items': medical_recs
        })
    
    # Metabolic recommendations
    metabolic_recs = []
    glucose = patient.get('avg_glucose_level', 0)
    if glucose > 125:
        metabolic_recs.extend([
            "Diabetes management and blood glucose monitoring",
            "HbA1c testing every 3-6 months",
            "Diabetic diet consultation"
        ])
    elif glucose > 100:
        metabolic_recs.extend([
            "Pre-diabetes monitoring and prevention",
            "Glucose tolerance testing",
            "Dietary modification to prevent diabetes"
        ])
    
    if metabolic_recs:
        recommendations.append({
            'category': 'Metabolic Health',
            'items': metabolic_recs
        })
    
    # Weight management
    bmi = patient.get('bmi', 0)
    if bmi >= 30:
        recommendations.append({
            'category': 'Weight Management',
            'items': [
                "Comprehensive weight loss program",
                "Nutritional counseling and meal planning",
                "Structured exercise program with medical clearance",
                "Consider bariatric consultation if BMI >40"
            ]
        })
    elif bmi >= 25:
        recommendations.append({
            'category': 'Weight Management',
            'items': [
                "Maintain healthy weight through diet and exercise",
                "Regular physical activity (150 min/week moderate exercise)",
                "Portion control and healthy eating habits"
            ]
        })
    
    # General recommendations
    recommendations.append({
        'category': 'General Prevention',
        'items': [
            "Regular blood pressure and glucose monitoring",
            "Heart-healthy diet (Mediterranean or DASH diet)",
            "Regular physical activity as medically appropriate",
            "Smoking cessation if applicable",
            "Limit alcohol consumption",
            "Stress management and adequate sleep"
        ]
    })
    
    # Display recommendations
    for rec_group in recommendations:
        st.markdown(f"### {rec_group['category']}")
        for item in rec_group['items']:
            st.markdown(f"""
            <div class="recommendation-box">
                🔹 {item}
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main results page function."""
    
    # Header
    st.markdown('<h1 class="main-header">📈 Risk Assessment Results</h1>', unsafe_allow_html=True)
    
    # DEBUG: Enhanced debug information
    if st.checkbox("🔧 Show Debug Information"):
        st.subheader("Debug Info")
        
        if st.session_state.prediction_results:
            st.write("**Prediction Results Found:**")
            results = st.session_state.prediction_results
            st.write(f"- Probability: {results.get('probability', 'Not found')}")
            st.write(f"- Probability Percent: {results.get('probability_percent', 'Not found')}")
            st.write(f"- Risk Level: '{results.get('risk_level', 'Not found')}'")
            st.write(f"- Success: {results.get('success', 'Not found')}")
            st.json(results)
        else:
            st.error("❌ No prediction results in session state!")
        
        if st.session_state.patient_data:
            st.write("**Patient Data Found:**")
            st.json(st.session_state.patient_data)
        else:
            st.error("❌ No patient data in session state!")
        
        st.write("---")
    
    # Check if results exist
    if not st.session_state.prediction_results:
        st.error("❌ No prediction results found.")
        st.info("Please complete the risk assessment first.")
        
        if st.button("📊 Go to Risk Assessment", use_container_width=True, type="primary"):
            st.switch_page("pages/risk_assessment.py")
        return
    
    # Verify data integrity
    results = st.session_state.prediction_results
    patient = st.session_state.patient_data
    
    # Check if essential data exists
    if not results.get('probability_percent') and results.get('probability_percent') != 0:
        st.error("❌ Invalid prediction results - missing probability data.")
        st.info("Please redo the risk assessment.")
        return
    
    if not results.get('risk_level'):
        st.error("❌ Invalid prediction results - missing risk level data.")
        st.info("Please redo the risk assessment.")
        return
    
    # Display patient summary
    display_patient_summary()
    
    st.divider()
    
    # Display risk analysis
    display_risk_analysis()
    
    st.divider()
    
    # Display detailed risk factors
    display_risk_factors()
    
    st.divider()
    
    # Display recommendations
    display_recommendations()
    
    st.divider()
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🆕 New Assessment", use_container_width=True):
            # Clear session state for new assessment
            st.session_state.prediction_results = None
            st.session_state.patient_data = None
            st.switch_page("pages/risk_assessment.py")
    
    with col2:
        if st.button("📊 Modify Assessment", use_container_width=True):
            st.switch_page("pages/risk_assessment.py")
    
    with col3:
        if st.button("💾 Download Report", use_container_width=True):
            # Generate downloadable report
            if st.session_state.prediction_results and st.session_state.patient_data:
                results = st.session_state.prediction_results
                patient = st.session_state.patient_data
                
                report_data = {
                    'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'patient_age': patient.get('age'),
                    'patient_gender': patient.get('gender', 'Unknown'),
                    'stroke_probability': f"{results.get('probability_percent', 0):.1f}%",
                    'risk_level': results.get('risk_level'),
                    'bmi': patient.get('bmi'),
                    'glucose_level': patient.get('avg_glucose_level'),
                    'hypertension': 'Yes' if patient.get('hypertension') else 'No',
                    'heart_disease': 'Yes' if patient.get('heart_disease') else 'No'
                }
                
                # Convert to downloadable format
                report_text = f"""
STROKE RISK ASSESSMENT REPORT
Generated: {report_data['assessment_date']}

PATIENT INFORMATION:
- Age: {report_data['patient_age']} years
- Gender: {report_data['patient_gender']}
- BMI: {report_data['bmi']}
- Glucose Level: {report_data['glucose_level']} mg/dL
- Hypertension: {report_data['hypertension']}
- Heart Disease: {report_data['heart_disease']}

RISK ASSESSMENT:
- Stroke Probability: {report_data['stroke_probability']}
- Risk Level: {report_data['risk_level']}

IMPORTANT: This assessment is for educational purposes only.
Consult healthcare providers for medical decisions.
                """
                
                st.download_button(
                    label="📄 Download Text Report",
                    data=report_text,
                    file_name=f"stroke_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    # Medical disclaimer
    st.markdown("""
    ---
    ### ⚠️ Important Medical Disclaimer
    
    This stroke risk assessment tool is for **educational and informational purposes only**. 
    It should not be used as a substitute for professional medical advice, diagnosis, or treatment. 
    
    **Always consult with qualified healthcare providers** regarding:
    - Medical conditions and symptoms
    - Treatment decisions
    - Medication changes
    - Lifestyle modifications
    
    Individual circumstances may significantly affect actual stroke risk beyond what this model can predict.
    """)

if __name__ == "__main__":
    main()