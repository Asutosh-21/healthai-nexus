import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from datetime import datetime
from auth_system.auth import AuthSystem
from core.preprocessor import InputPreprocessor
from core.triage_agent import TriageAgent
from core.orchestrator import Orchestrator
from core.aggregator import Aggregator
from database.database import Database
from utils.ocr_reader import extract_text_from_file
from agents.wellness_agent import WellnessAgent
from services.treatment_recommender import TreatmentRecommender
from generators.prescription_generator import PrescriptionGenerator

# Page config
st.set_page_config(
    page_title="HealthAI Nexus",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .sidebar .element-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize systems
auth = AuthSystem()
db = Database()

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# Login/Register Page
if not st.session_state.logged_in:
    st.markdown('<div class="main-header"><h1>🏥 HealthAI Nexus</h1><p>AI-Powered Healthcare Assistant</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", key="login_btn"):
                if username and password:
                    success, user_data = auth.login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = user_data
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Please enter username and password")
        
        with tab2:
            st.markdown("### Create Account")
            new_username = st.text_input("Username", key="reg_user")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Password", type="password", key="reg_pass")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Register", key="reg_btn"):
                if new_username and new_password:
                    if new_password == confirm_password:
                        success, message = auth.register(new_username, new_password, new_email)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("Passwords don't match")
                else:
                    st.warning("Please fill all fields")

# Main Dashboard
else:
    # Initialize components
    preprocessor = InputPreprocessor()
    triage = TriageAgent()
    orchestrator = Orchestrator()
    aggregator = Aggregator()
    wellness_agent = WellnessAgent()
    treatment_recommender = TreatmentRecommender()
    prescription_gen = PrescriptionGenerator()
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="main-header"><h1>🏥 HealthAI Nexus</h1><p>Welcome, {st.session_state.user["username"]}!</p></div>', unsafe_allow_html=True)
    with col2:
        st.write("")
        st.write("")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.analysis_done = False
            st.rerun()
    
    # Sidebar - Patient Profile
    with st.sidebar:
        st.markdown("### 👤 Personal Information")
        
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=30, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
        with col2:
            weight_lbs = weight * 2.20462
            st.metric("Weight (lbs)", f"{weight_lbs:.1f}")
        
        col1, col2 = st.columns(2)
        with col1:
            height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.1)
        with col2:
            height_inch = height_cm / 2.54
            height_ft = int(height_inch // 12)
            height_in = height_inch % 12
            st.metric("Height (ft.in)", f"{height_ft}'{height_in:.1f}\"")
        
        # Calculate BMI
        bmi = weight / ((height_cm/100) ** 2)
        
        # BMI Category
        if bmi < 18.5:
            bmi_category = "Underweight"
            bmi_color = "🔵"
        elif 18.5 <= bmi < 25:
            bmi_category = "Normal"
            bmi_color = "🟢"
        elif 25 <= bmi < 30:
            bmi_category = "Overweight"
            bmi_color = "🟡"
        else:
            bmi_category = "Obese"
            bmi_color = "🔴"
        
        st.metric("BMI", f"{bmi:.1f}", f"{bmi_color} {bmi_category}")
        
        # Health Reference Chart
        with st.expander("📊 Health Reference Guide"):
            st.markdown("**BMI Categories:**")
            st.markdown("""
            - 🔵 Underweight: < 18.5
            - 🟢 Normal: 18.5 - 24.9
            - 🟡 Overweight: 25 - 29.9
            - 🔴 Obese: ≥ 30
            """)
            
            st.markdown("**Ideal Weight Range:**")
            height_m = height_cm / 100
            ideal_min = 18.5 * (height_m ** 2)
            ideal_max = 24.9 * (height_m ** 2)
            ideal_min_lbs = ideal_min * 2.20462
            ideal_max_lbs = ideal_max * 2.20462
            st.info(f"For {height_ft}'{height_in:.0f}\": {ideal_min:.1f}-{ideal_max:.1f} kg ({ideal_min_lbs:.0f}-{ideal_max_lbs:.0f} lbs)")
            
            st.markdown("**Age-Based Health Metrics:**")
            if age < 18:
                st.write("👶 Youth: Growth phase, consult pediatrician")
            elif 18 <= age < 40:
                st.write("💪 Adult: Maintain healthy lifestyle")
            elif 40 <= age < 65:
                st.write("🧘 Middle Age: Regular health checkups")
            else:
                st.write("👴 Senior: Comprehensive health monitoring")
        
        st.markdown("---")
        st.markdown("### 🚨 Medical History")
        allergies = st.text_area("Allergies", placeholder="e.g., penicillin, peanuts", height=60)
        current_meds = st.text_area("Current Medications", placeholder="e.g., aspirin, metformin", height=60)
        conditions = st.text_area("Existing Conditions", placeholder="e.g., diabetes, hypertension", height=60)
        
        # Save profile
        st.session_state.patient_profile = {
            'username': st.session_state.user['username'],
            'age': age,
            'weight': weight,
            'weight_lbs': weight_lbs,
            'height': height_cm,
            'height_inch': height_inch,
            'height_ft': f"{height_ft}'{height_in:.1f}\"",
            'bmi': bmi,
            'bmi_category': bmi_category,
            'allergies': [a.strip() for a in allergies.split(',') if a.strip()],
            'current_medications': [m.strip() for m in current_meds.split(',') if m.strip()],
            'conditions': [c.strip() for c in conditions.split(',') if c.strip()]
        }
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🩺 Analysis", "💊 Treatment", "🌱 Wellness", "📄 Prescription"])
    
    # TAB 1: Dashboard
    with tab1:
        st.markdown("### 📊 Health Overview Dashboard")
        
        # Personal Health Metrics Card
        st.markdown("#### 👤 Your Health Profile")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Age", f"{age} yrs")
        with col2:
            st.metric("Weight", f"{weight:.1f} kg", f"{weight_lbs:.1f} lbs")
        with col3:
            st.metric("Height", f"{height_cm:.0f} cm", f"{height_ft}'{height_in:.1f}\"")
        with col4:
            st.metric("BMI", f"{bmi:.1f}", f"{bmi_category}")
        with col5:
            health_score = max(0, 100 - (abs(bmi - 22) * 5))
            st.metric("Health Score", f"{health_score:.0f}/100")
        
        st.markdown("---")
        
        # Get user reports
        user_reports = db.get_all_reports(limit=10)
        
        if user_reports:
            # Analysis Metrics
            st.markdown("#### 📈 Analysis Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Analyses", len(user_reports), "📋")
            with col2:
                avg_risk = sum([r['risk_score'] for r in user_reports]) / len(user_reports)
                risk_trend = "↓" if len(user_reports) > 1 and user_reports[0]['risk_score'] < user_reports[1]['risk_score'] else "↑"
                st.metric("Avg Risk Score", f"{avg_risk:.1f}/10", risk_trend)
            with col3:
                last_analysis = user_reports[0]['timestamp'][:10]
                st.metric("Last Analysis", last_analysis, "📅")
            with col4:
                high_risk_count = len([r for r in user_reports if r['risk_score'] > 6])
                st.metric("High Risk Cases", high_risk_count, "⚠️")
            
            st.markdown("---")
            st.markdown("#### 📊 Visual Analytics")
            
            # Prepare data
            df = pd.DataFrame(user_reports)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Charts Row 1
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk score trend with markers
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['timestamp'], 
                    y=df['risk_score'],
                    mode='lines+markers',
                    name='Risk Score',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=10, color=df['risk_score'], 
                               colorscale='RdYlGn_r', showscale=True,
                               colorbar=dict(title="Risk"))
                ))
                fig.update_layout(
                    title='📈 Risk Score Trend Over Time',
                    xaxis_title='Date',
                    yaxis_title='Risk Score (0-10)',
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Risk distribution pie chart
                risk_categories = ['🟢 Low (0-3)', '🟡 Medium (4-6)', '🔴 High (7-10)']
                risk_counts = [
                    len([r for r in user_reports if r['risk_score'] <= 3]),
                    len([r for r in user_reports if 3 < r['risk_score'] <= 6]),
                    len([r for r in user_reports if r['risk_score'] > 6])
                ]
                
                fig = go.Figure(data=[go.Pie(
                    labels=risk_categories, 
                    values=risk_counts,
                    marker=dict(colors=['#28a745', '#ffc107', '#dc3545']),
                    hole=0.4,
                    textinfo='label+percent',
                    textfont_size=12
                )])
                fig.update_layout(
                    title='🎯 Risk Category Distribution',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Charts Row 2
            col1, col2 = st.columns(2)
            
            with col1:
                # BMI tracking over time (if available)
                fig = go.Figure()
                fig.add_trace(go.Indicator(
                    mode="gauge+number+delta",
                    value=bmi,
                    title={'text': "Current BMI"},
                    delta={'reference': 22, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                    gauge={
                        'axis': {'range': [None, 40]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 18.5], 'color': "lightblue"},
                            {'range': [18.5, 25], 'color': "lightgreen"},
                            {'range': [25, 30], 'color': "yellow"},
                            {'range': [30, 40], 'color': "red"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 30}
                    }
                ))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Analysis frequency by month
                df['month'] = df['timestamp'].dt.to_period('M').astype(str)
                monthly_counts = df.groupby('month').size().reset_index(name='count')
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=monthly_counts['month'],
                        y=monthly_counts['count'],
                        marker_color='#667eea',
                        text=monthly_counts['count'],
                        textposition='auto'
                    )
                ])
                fig.update_layout(
                    title='📅 Analysis Frequency by Month',
                    xaxis_title='Month',
                    yaxis_title='Number of Analyses',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent reports table with better formatting
            st.markdown("---")
            st.markdown("#### 📋 Recent Analysis Reports")
            
            df_display = df[['id', 'timestamp', 'symptoms', 'risk_score']].copy()
            df_display['timestamp'] = df_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            df_display['symptoms'] = df_display['symptoms'].str[:60] + '...'
            df_display['risk_level'] = df_display['risk_score'].apply(
                lambda x: '🟢 Low' if x <= 3 else '🟡 Medium' if x <= 6 else '🔴 High'
            )
            df_display = df_display.rename(columns={
                'id': 'Report ID',
                'timestamp': 'Date & Time',
                'symptoms': 'Symptoms',
                'risk_score': 'Risk Score',
                'risk_level': 'Risk Level'
            })
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Risk Score": st.column_config.ProgressColumn(
                        "Risk Score",
                        help="Risk score from 0-10",
                        format="%.1f",
                        min_value=0,
                        max_value=10,
                    )
                }
            )
        else:
            st.info("📝 No analysis reports yet. Start by analyzing your symptoms in the Analysis tab!")
            
            # Show health tips for new users
            st.markdown("#### 💡 Health Tips")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("**🥗 Nutrition**\n\nMaintain balanced diet with fruits, vegetables, and whole grains")
            with col2:
                st.info("**🏃 Exercise**\n\n30 minutes of moderate activity daily for optimal health")
            with col3:
                st.info("**😴 Sleep**\n\n7-9 hours of quality sleep per night is essential")
    
    # TAB 2: Analysis
    with tab2:
        st.markdown("### 🩺 Symptom Analysis")
        
        symptoms = st.text_area("Describe your symptoms:", height=150, 
                               placeholder="e.g., High fever, cough, sore throat...")
        
        uploaded_file = st.file_uploader("Upload Medical Report (Optional)", 
                                        type=["jpg", "png", "pdf", "txt"])
        
        if uploaded_file:
            extracted_text = extract_text_from_file(uploaded_file)
            if extracted_text:
                st.success("✅ File processed")
                with st.expander("View extracted text"):
                    st.text(extracted_text[:300])
        
        if st.button("🔍 Analyze Symptoms", type="primary"):
            if symptoms:
                with st.spinner("Analyzing..."):
                    processed = preprocessor.process(symptoms)
                    specialists = triage.route(processed)
                    
                    st.info(f"Consulting: {', '.join([s.replace('_', ' ').title() for s in specialists])}")
                    
                    agent_results = orchestrator.execute(specialists, processed)
                    synthesis_result = aggregator.synthesize(agent_results, processed)
                    risk_score = aggregator.calculate_risk_score(agent_results)
                    
                    st.session_state.analysis_done = True
                    st.session_state.agent_results = agent_results
                    st.session_state.synthesis = synthesis_result['synthesis']
                    st.session_state.risk_score = risk_score
                    st.session_state.symptoms = symptoms
                    
                    report_data = {
                        'symptoms': symptoms,
                        'risk_score': risk_score,
                        'synthesis': synthesis_result['synthesis'],
                        'evidence': synthesis_result['evidence'],
                        'specialist_reports': agent_results
                    }
                    report_id = db.save_report(report_data)
                    st.session_state.report_id = report_id
                    
                    # Auto-save reports to outputs folder
                    import os
                    import json
                    from generators.report_generator import ReportGenerator
                    
                    os.makedirs("outputs/reports", exist_ok=True)
                    os.makedirs("outputs/pdfs", exist_ok=True)
                    
                    # Save JSON report
                    json_file = f"outputs/reports/report_{report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(json_file, 'w') as f:
                        json.dump(report_data, f, indent=2)
                    
                    # Save PDF report
                    pdf_file = f"outputs/pdfs/report_{report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    try:
                        ReportGenerator.generate_pdf(report_data, pdf_file)
                    except:
                        pass
                
                st.success(f"✅ Analysis Complete! Reports auto-saved to outputs folder.")
                st.info(f"📁 JSON: outputs/reports/report_{report_id}_*.json\n📄 PDF: outputs/pdfs/report_{report_id}_*.pdf")
                st.rerun()
        
        if st.session_state.analysis_done:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Risk Score", f"{st.session_state.risk_score}/10")
            with col2:
                st.metric("Specialists", len(st.session_state.agent_results))
            with col3:
                st.metric("Report ID", st.session_state.report_id)
            
            st.markdown("### 🔬 Medical Assessment")
            
            # Create expandable sections for better readability
            with st.expander("📄 Full Assessment Report", expanded=True):
                st.success(st.session_state.synthesis)
            
            # Show specialist breakdown
            with st.expander("👨⚕️ Specialist Consultations"):
                for specialist, report in st.session_state.agent_results.items():
                    st.markdown(f"**{specialist.replace('_', ' ').title()}:**")
                    st.write(report[:300] + "..." if len(report) > 300 else report)
                    st.markdown("---")
    
    # TAB 3: Treatment
    with tab3:
        if st.session_state.analysis_done:
            st.markdown("### 💊 Comprehensive Treatment Plan")
            
            treatment = treatment_recommender.recommend_treatment(
                st.session_state.synthesis,
                st.session_state.patient_profile
            )
            
            # Doctor's Advice Section
            st.markdown("#### 👨‍⚕️ Doctor's Advice")
            with st.expander("📋 Medical Recommendations", expanded=True):
                st.info(f"""
                **Based on your symptoms and health profile:**
                
                - Age: {st.session_state.patient_profile['age']} years
                - BMI: {st.session_state.patient_profile['bmi']:.1f} ({st.session_state.patient_profile['bmi_category']})
                - Risk Level: {st.session_state.risk_score}/10
                
                **Immediate Actions:**
                1. Follow prescribed medication schedule strictly
                2. Monitor symptoms daily
                3. Maintain proper hydration (8-10 glasses water/day)
                4. Get adequate rest (7-9 hours sleep)
                5. Avoid self-medication
                """)
            
            # Prescribed Medications
            st.markdown("#### 💊 Prescribed Medications")
            if treatment.get('medications'):
                for idx, med in enumerate(treatment['medications'], 1):
                    with st.expander(f"💊 {idx}. {med.get('name', 'N/A').upper()}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**📋 Prescription Details**")
                            st.write(f"**Generic Name:** {med.get('name', 'N/A')}")
                            st.write(f"**Dosage:** {med.get('dosage', 'N/A')}")
                            st.write(f"**Frequency:** {med.get('frequency', 'N/A')}")
                            st.write(f"**Duration:** {med.get('duration', 'N/A')}")
                        
                        with col2:
                            st.markdown("**⚕️ Usage Instructions**")
                            st.write("• Take with food" if "food" in med.get('name', '').lower() else "• Can take on empty stomach")
                            st.write("• Do not skip doses")
                            st.write("• Complete full course")
                            st.write("• Store in cool, dry place")
                        
                        with col3:
                            st.markdown("**⚠️ Safety Information**")
                            if 'safety_check' in med:
                                safety = med['safety_check']['safety']
                                if safety == "Safe":
                                    st.success("✅ Safe to use")
                                elif safety == "Caution":
                                    st.warning("⚠️ Use with caution")
                                else:
                                    st.error("❌ Contraindicated")
                                
                                if med['safety_check'].get('warnings'):
                                    for warning in med['safety_check']['warnings'][:2]:
                                        st.write(f"⚠️ {warning}")
                        
                        # Side Effects
                        st.markdown("**🔍 Common Side Effects:**")
                        st.write("• Mild nausea or stomach upset")
                        st.write("• Drowsiness or dizziness")
                        st.write("• Headache")
                        st.caption("*Consult doctor if side effects persist*")
            
            # Non-Pharmacological Treatment
            st.markdown("---")
            st.markdown("#### 🌿 Non-Pharmacological Treatment")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🏠 Home Remedies:**")
                if treatment.get('non_pharmacological'):
                    for item in treatment['non_pharmacological'][:3]:
                        st.write(f"• {item}")
                else:
                    st.write("• Rest and adequate sleep")
                    st.write("• Stay hydrated")
                    st.write("• Warm compress if needed")
            
            with col2:
                st.markdown("**📊 Monitoring Requirements:**")
                if treatment.get('monitoring'):
                    for item in treatment['monitoring'][:3]:
                        st.write(f"• {item}")
                else:
                    st.write("• Track symptoms daily")
                    st.write("• Monitor temperature")
                    st.write("• Note any changes")
            
            # Follow-up Schedule
            st.markdown("---")
            st.markdown("#### 📅 Follow-up Schedule")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("**🔔 Day 3**\n\nCheck symptom improvement")
            with col2:
                st.info("**🔔 Day 7**\n\nReview medication response")
            with col3:
                st.info("**🔔 Day 14**\n\nFinal assessment")
            
            # Emergency Warning
            st.markdown("---")
            st.error("""
            **🚨 SEEK IMMEDIATE MEDICAL ATTENTION IF:**
            - Symptoms worsen rapidly
            - Difficulty breathing
            - Severe chest pain
            - High fever (>103°F) not responding to medication
            - Severe allergic reaction (rash, swelling, difficulty breathing)
            """)
            
        else:
            st.warning("⚠️ Complete symptom analysis first in the Analysis tab")
    
    # TAB 4: Wellness
    with tab4:
        if st.session_state.analysis_done:
            st.markdown("### 🌱 Comprehensive Wellness & Preventive Care Plan")
            
            wellness = wellness_agent.run(st.session_state.synthesis)
            
            if isinstance(wellness, dict) and 'diet' in wellness:
                # Nutrition Plan
                st.markdown("#### 🥗 Personalized Nutrition Plan")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**✅ Foods to Eat**")
                    with st.container():
                        for food in wellness['diet'].get('foods_to_eat', [])[:6]:
                            st.success(f"✓ {food}")
                
                with col2:
                    st.markdown("**❌ Foods to Avoid**")
                    with st.container():
                        for food in wellness['diet'].get('foods_to_avoid', [])[:6]:
                            st.error(f"✗ {food}")
                
                with col3:
                    st.markdown("**💧 Hydration & Timing**")
                    st.info(wellness['diet'].get('hydration', 'Drink 8-10 glasses of water daily'))
                    st.write("**Meal Schedule:**")
                    st.write("• Breakfast: 7-9 AM")
                    st.write("• Lunch: 12-2 PM")
                    st.write("• Dinner: 6-8 PM")
                    st.write("• Snacks: Healthy options")
                
                # Exercise & Fitness
                st.markdown("---")
                st.markdown("#### 🏃 Exercise & Fitness Routine")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📋 Recommended Exercises**")
                    ex = wellness.get('exercise', {})
                    st.write(f"**Type:** {ex.get('type', 'Moderate aerobic activity')}")
                    st.write(f"**Duration:** {ex.get('duration', '30 minutes')}")
                    st.write(f"**Frequency:** {ex.get('frequency', '5 days/week')}")
                    
                    st.markdown("**Weekly Schedule:**")
                    st.write("• Monday: Cardio (30 min)")
                    st.write("• Tuesday: Strength training")
                    st.write("• Wednesday: Yoga/Stretching")
                    st.write("• Thursday: Cardio (30 min)")
                    st.write("• Friday: Strength training")
                    st.write("• Weekend: Light activity/Rest")
                
                with col2:
                    st.markdown("**⚠️ Exercise Precautions**")
                    if ex.get('precautions'):
                        for precaution in ex['precautions']:
                            st.warning(f"⚠️ {precaution}")
                    else:
                        st.warning("⚠️ Start slowly and gradually increase intensity")
                        st.warning("⚠️ Stop if you feel dizzy or short of breath")
                        st.warning("⚠️ Stay hydrated during exercise")
                    
                    st.markdown("**💪 Fitness Goals**")
                    st.info("• Improve cardiovascular health")
                    st.info("• Maintain healthy weight")
                    st.info("• Increase strength & flexibility")
                    st.info("• Reduce stress levels")
                
                # Lifestyle Modifications
                st.markdown("---")
                st.markdown("#### 🌙 Lifestyle & Daily Habits")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**😴 Sleep Hygiene**")
                    ls = wellness.get('lifestyle', {})
                    st.write(ls.get('sleep', '7-9 hours of quality sleep'))
                    st.write("\n**Sleep Tips:**")
                    st.write("• Consistent sleep schedule")
                    st.write("• Dark, cool bedroom")
                    st.write("• No screens 1hr before bed")
                    st.write("• Relaxing bedtime routine")
                
                with col2:
                    st.markdown("**🧘 Stress Management**")
                    if ls.get('stress_management'):
                        for tip in ls['stress_management'][:4]:
                            st.write(f"• {tip}")
                    else:
                        st.write("• Deep breathing exercises")
                        st.write("• Meditation (10-15 min/day)")
                        st.write("• Yoga or tai chi")
                        st.write("• Journaling")
                
                with col3:
                    st.markdown("**✨ Healthy Habits**")
                    if ls.get('habits'):
                        for habit in ls['habits'][:4]:
                            st.write(f"• {habit}")
                    else:
                        st.write("• Quit smoking")
                        st.write("• Limit alcohol")
                        st.write("• Regular health checkups")
                        st.write("• Maintain social connections")
                
                # Preventive Care
                st.markdown("---")
                st.markdown("#### 🛡️ Preventive Health Measures")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**🔬 Recommended Screenings**")
                    prev = wellness.get('preventive', {})
                    if prev.get('screenings'):
                        for screening in prev['screenings']:
                            st.write(f"• {screening}")
                    else:
                        st.write("• Annual physical exam")
                        st.write("• Blood pressure check")
                        st.write("• Blood sugar test")
                        st.write("• Cholesterol screening")
                
                with col2:
                    st.markdown("**💊 Supplements (if needed)**")
                    if prev.get('supplements'):
                        for supplement in prev['supplements']:
                            st.write(f"• {supplement}")
                    else:
                        st.write("• Vitamin D (if deficient)")
                        st.write("• Omega-3 fatty acids")
                        st.write("• Multivitamin")
                        st.write("• Probiotics")
                    st.caption("*Consult doctor before taking supplements*")
                
                with col3:
                    st.markdown("**📅 Follow-up Timeline**")
                    st.info(prev.get('follow_up', 'Regular checkups every 3-6 months'))
                    st.write("\n**Vaccination Updates:**")
                    st.write("• Flu shot (annual)")
                    st.write("• COVID-19 booster")
                    st.write("• Tetanus (every 10 years)")
                
                # Mental Health
                st.markdown("---")
                st.markdown("#### 🧠 Mental Health & Well-being")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info("""
                    **🌟 Mental Wellness Tips:**
                    - Practice mindfulness daily
                    - Stay connected with loved ones
                    - Engage in hobbies you enjoy
                    - Seek professional help if needed
                    - Maintain work-life balance
                    """)
                
                with col2:
                    st.success("""
                    **😊 Positive Lifestyle Changes:**
                    - Set realistic health goals
                    - Track your progress
                    - Celebrate small victories
                    - Stay motivated and consistent
                    - Join support groups if helpful
                    """)
                
                # Health Score Progress
                st.markdown("---")
                st.markdown("#### 📈 Your Wellness Score")
                
                # Calculate wellness score
                wellness_score = 70  # Base score
                if st.session_state.patient_profile['bmi_category'] == 'Normal':
                    wellness_score += 15
                elif st.session_state.patient_profile['bmi_category'] in ['Overweight', 'Underweight']:
                    wellness_score += 5
                
                if st.session_state.risk_score <= 3:
                    wellness_score += 15
                elif st.session_state.risk_score <= 6:
                    wellness_score += 10
                
                import plotly.graph_objects as go
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=wellness_score,
                    title={'text': "Overall Wellness Score"},
                    delta={'reference': 80},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkgreen"},
                        'steps': [
                            {'range': [0, 40], 'color': "lightcoral"},
                            {'range': [40, 70], 'color': "lightyellow"},
                            {'range': [70, 100], 'color': "lightgreen"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90}
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                st.info(f"**Your Score: {wellness_score}/100** - {'Excellent!' if wellness_score >= 80 else 'Good progress!' if wellness_score >= 60 else 'Keep improving!'}")
            
        else:
            st.warning("⚠️ Complete symptom analysis first in the Analysis tab")
    
    # TAB 5: Prescription
    with tab5:
        if st.session_state.analysis_done:
            st.markdown("### 📄 AI-Generated Prescription")
            
            if st.button("Generate Prescription"):
                with st.spinner("Generating prescription..."):
                    prescription_text = prescription_gen.generate_prescription(
                        st.session_state.patient_profile,
                        st.session_state.synthesis,
                        str(st.session_state.agent_results)
                    )
                    
                    st.text_area("Prescription", prescription_text, height=300)
                    
                    # Generate and auto-save PDF
                    import os
                    os.makedirs("outputs/prescriptions", exist_ok=True)
                    pdf_file = f"outputs/prescriptions/prescription_{st.session_state.report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    prescription_gen.create_prescription_pdf(
                        st.session_state.patient_profile,
                        prescription_text,
                        pdf_file
                    )
                    
                    # Also save prescription text
                    txt_file = f"outputs/prescriptions/prescription_{st.session_state.report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(txt_file, 'w', encoding='utf-8') as f:
                        f.write(f"PRESCRIPTION - {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
                        f.write("="*80 + "\n\n")
                        f.write(f"Patient: {st.session_state.patient_profile['username']}\n")
                        f.write(f"Age: {st.session_state.patient_profile['age']} years\n")
                        f.write(f"BMI: {st.session_state.patient_profile['bmi']:.1f}\n\n")
                        f.write(prescription_text)
                        f.write("\n\n" + "="*80 + "\n")
                        f.write("⚠️ DISCLAIMER: AI-generated for informational purposes only.\n")
                        f.write("NOT a valid legal prescription. Consult healthcare provider.\n")
                    
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            "📥 Download Prescription PDF",
                            data=f,
                            file_name=f"prescription_{st.session_state.report_id}.pdf",
                            mime="application/pdf"
                        )
                    
                    st.success(f"✅ Prescription auto-saved to: {pdf_file}")
                    
                    st.error("⚠️ **DISCLAIMER:** This is an AI-generated prescription for informational purposes only. NOT a valid legal prescription. Consult a licensed healthcare provider.")
        else:
            st.warning("Complete symptom analysis first")
    
    # Footer
    st.markdown("---")
    st.caption("⚠️ AI assistant for informational purposes only. Consult healthcare professionals for medical decisions.")
