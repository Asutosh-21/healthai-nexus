import streamlit as st
from preprocessor import InputPreprocessor
from triage_agent import TriageAgent
from orchestrator import Orchestrator
from aggregator import Aggregator
from report_generator import ReportGenerator
from database import Database
from utils.ocr_reader import extract_text_from_file
from agents.wellness_agent import WellnessAgent
from treatment_recommender import TreatmentRecommender
import json

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
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .section-header {
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'patient_profile' not in st.session_state:
    st.session_state.patient_profile = {}

# Initialize components
db = Database()
preprocessor = InputPreprocessor()
triage = TriageAgent()
orchestrator = Orchestrator()
aggregator = Aggregator()
wellness_agent = WellnessAgent()
treatment_recommender = TreatmentRecommender()

# Sidebar - Patient Profile
with st.sidebar:
    st.markdown("### 👤 Patient Profile")
    
    age = st.selectbox("Age Group", ["Child (0-12)", "Teen (13-17)", "Adult (18-64)", "Senior (65+)"], index=2)
    weight = st.selectbox("Weight Category", ["Underweight", "Normal", "Overweight", "Obese"], index=1)
    
    st.markdown("### 🚨 Medical History")
    allergies = st.text_input("Allergies (comma-separated)", placeholder="e.g., penicillin, peanuts")
    current_meds = st.text_input("Current Medications", placeholder="e.g., aspirin, metformin")
    conditions = st.text_input("Existing Conditions", placeholder="e.g., diabetes, hypertension")
    
    # Save profile
    st.session_state.patient_profile = {
        'age': age,
        'weight': weight,
        'allergies': [a.strip() for a in allergies.split(',') if a.strip()],
        'current_medications': [m.strip() for m in current_meds.split(',') if m.strip()],
        'conditions': [c.strip() for c in conditions.split(',') if c.strip()]
    }
    
    st.markdown("---")
    st.markdown("### 📋 Recent Reports")
    recent_reports = db.get_all_reports(limit=3)
    if recent_reports:
        for report in recent_reports:
            with st.expander(f"Report #{report['id']}"):
                st.caption(report['timestamp'][:16])
                st.write(f"Risk: {report['risk_score']}/10")
    else:
        st.info("No reports yet")

# Main header
st.markdown('<div class="main-header">🏥 HealthAI Nexus</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">AI-Powered Multi-Agent Healthcare System</p>', unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🩺 Symptom Analysis", "💊 Treatment Plan", "🌱 Wellness Plan", "📊 Reports"])

# TAB 1: Symptom Analysis
with tab1:
    st.markdown('<div class="section-header"><h2>🩺 Symptom Analysis</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symptoms = st.text_area(
            "Describe your symptoms in detail:",
            height=150,
            placeholder="e.g., I have a high fever, cough, and body aches for 3 days..."
        )
    
    with col2:
        uploaded_file = st.file_uploader(
            "Upload Medical Report (Optional)",
            type=["jpg", "png", "pdf", "txt"],
            help="Upload lab reports, prescriptions, or medical documents"
        )
        
        if uploaded_file:
            with st.spinner("Reading file..."):
                extracted_text = extract_text_from_file(uploaded_file)
                if extracted_text:
                    st.success("✅ File processed")
                    with st.expander("View extracted text"):
                        st.text(extracted_text[:300] + "...")
    
    if st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True):
        if not symptoms and not uploaded_file:
            st.error("Please enter symptoms or upload a report")
        else:
            # Combine inputs
            full_input = symptoms
            if uploaded_file and extracted_text:
                full_input += f"\n\nExtracted from file:\n{extracted_text}"
            
            with st.spinner("🔄 Processing..."):
                # Preprocess
                processed_input = preprocessor.process(full_input)
                
                # Triage
                selected_specialists = triage.route(processed_input)
                st.info(f"🩺 Consulting: {', '.join([s.replace('_', ' ').title() for s in selected_specialists])}")
                
                # Execute agents
                progress_bar = st.progress(0)
                agent_results = orchestrator.execute(selected_specialists, processed_input)
                progress_bar.progress(100)
                
                # Aggregate
                synthesis_result = aggregator.synthesize(agent_results, processed_input)
                risk_score = aggregator.calculate_risk_score(agent_results)
                
                # Store in session
                st.session_state.analysis_done = True
                st.session_state.agent_results = agent_results
                st.session_state.synthesis = synthesis_result['synthesis']
                st.session_state.evidence = synthesis_result['evidence']
                st.session_state.risk_score = risk_score
                st.session_state.symptoms = symptoms
                
                # Save to DB
                report_data = {
                    'symptoms': symptoms,
                    'risk_score': risk_score,
                    'synthesis': synthesis_result['synthesis'],
                    'evidence': synthesis_result['evidence'],
                    'specialist_reports': agent_results
                }
                report_id = db.save_report(report_data)
                st.session_state.report_id = report_id
            
            st.success("✅ Analysis Complete!")
            st.rerun()
    
    # Display results
    if st.session_state.analysis_done:
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            risk_color = "🔴" if st.session_state.risk_score > 7 else "🟡" if st.session_state.risk_score > 3 else "🟢"
            st.metric("Risk Score", f"{risk_color} {st.session_state.risk_score}/10")
        with col2:
            st.metric("Specialists", len(st.session_state.agent_results))
        with col3:
            st.metric("Report ID", st.session_state.report_id)
        with col4:
            urgency = "High" if st.session_state.risk_score > 7 else "Medium" if st.session_state.risk_score > 3 else "Low"
            st.metric("Urgency", urgency)
        
        # Synthesis
        st.markdown("### 🔬 Medical Assessment")
        st.success(st.session_state.synthesis)
        
        # Evidence
        with st.expander("📚 Evidence-Based Information"):
            st.info(st.session_state.evidence)
        
        # Specialist reports
        with st.expander("👨‍⚕️ Specialist Consultations"):
            for specialist, report in st.session_state.agent_results.items():
                st.markdown(f"**{specialist.replace('_', ' ').title()}:**")
                st.write(report)
                st.markdown("---")

# TAB 2: Treatment Plan
with tab2:
    st.markdown('<div class="section-header"><h2>💊 Personalized Treatment Plan</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.analysis_done:
        st.warning("⚠️ Please complete symptom analysis first (Tab 1)")
    else:
        with st.spinner("Generating personalized treatment plan..."):
            treatment_plan = treatment_recommender.recommend_treatment(
                st.session_state.synthesis,
                st.session_state.patient_profile
            )
        
        # Medications
        st.markdown("### 💊 Recommended Medications")
        if treatment_plan.get('medications'):
            for idx, med in enumerate(treatment_plan['medications'], 1):
                with st.expander(f"💊 {idx}. {med.get('name', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Dosage:** {med.get('dosage', 'N/A')}")
                        st.write(f"**Frequency:** {med.get('frequency', 'N/A')}")
                        st.write(f"**Duration:** {med.get('duration', 'N/A')}")
                    with col2:
                        if 'safety_check' in med:
                            safety = med['safety_check']
                            safety_status = safety.get('safety', 'Unknown')
                            color = "green" if safety_status == "Safe" else "orange" if safety_status == "Caution" else "red"
                            st.markdown(f"**Safety:** :{color}[{safety_status}]")
                            if safety.get('warnings'):
                                st.warning("⚠️ " + ", ".join(safety['warnings'][:2]))
        else:
            st.info("No specific medications recommended. Consult healthcare provider.")
        
        # Non-pharmacological
        st.markdown("### 🌿 Non-Pharmacological Treatments")
        if treatment_plan.get('non_pharmacological'):
            for treatment in treatment_plan['non_pharmacological']:
                st.write(f"• {treatment}")
        
        # Monitoring
        st.markdown("### 📈 Monitoring Requirements")
        if treatment_plan.get('monitoring'):
            for item in treatment_plan['monitoring']:
                st.write(f"• {item}")
        
        # Precautions
        with st.expander("⚠️ Important Precautions"):
            if treatment_plan.get('precautions'):
                for precaution in treatment_plan['precautions']:
                    st.warning(precaution)

# TAB 3: Wellness Plan
with tab3:
    st.markdown('<div class="section-header"><h2>🌱 Preventive Health & Wellness Plan</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.analysis_done:
        st.warning("⚠️ Please complete symptom analysis first (Tab 1)")
    else:
        with st.spinner("Creating personalized wellness plan..."):
            wellness_plan = wellness_agent.run(st.session_state.synthesis)
        
        if isinstance(wellness_plan, dict) and 'raw_plan' not in wellness_plan:
            # Diet Plan
            st.markdown("### 🥗 Personalized Diet Plan")
            if 'diet' in wellness_plan:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ Foods to Eat:**")
                    for food in wellness_plan['diet'].get('foods_to_eat', []):
                        st.write(f"• {food}")
                with col2:
                    st.markdown("**❌ Foods to Avoid:**")
                    for food in wellness_plan['diet'].get('foods_to_avoid', []):
                        st.write(f"• {food}")
                
                st.info(f"💧 **Hydration:** {wellness_plan['diet'].get('hydration', 'Drink 8 glasses of water daily')}")
            
            # Exercise
            st.markdown("### 🏃 Exercise Routine")
            if 'exercise' in wellness_plan:
                ex = wellness_plan['exercise']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Type", ex.get('type', 'N/A'))
                with col2:
                    st.metric("Duration", ex.get('duration', 'N/A'))
                with col3:
                    st.metric("Frequency", ex.get('frequency', 'N/A'))
                
                if ex.get('precautions'):
                    with st.expander("⚠️ Exercise Precautions"):
                        for precaution in ex['precautions']:
                            st.write(f"• {precaution}")
            
            # Lifestyle
            st.markdown("### 🌙 Lifestyle Modifications")
            if 'lifestyle' in wellness_plan:
                ls = wellness_plan['lifestyle']
                st.write(f"**Sleep:** {ls.get('sleep', 'N/A')}")
                
                if ls.get('stress_management'):
                    st.markdown("**Stress Management:**")
                    for tip in ls['stress_management']:
                        st.write(f"• {tip}")
                
                if ls.get('habits'):
                    st.markdown("**Healthy Habits:**")
                    for habit in ls['habits']:
                        st.write(f"• {habit}")
            
            # Preventive
            st.markdown("### 🛡️ Preventive Measures")
            if 'preventive' in wellness_plan:
                prev = wellness_plan['preventive']
                
                col1, col2 = st.columns(2)
                with col1:
                    if prev.get('screenings'):
                        st.markdown("**Recommended Screenings:**")
                        for screening in prev['screenings']:
                            st.write(f"• {screening}")
                
                with col2:
                    if prev.get('supplements'):
                        st.markdown("**Supplements:**")
                        for supplement in prev['supplements']:
                            st.write(f"• {supplement}")
                
                st.info(f"📅 **Follow-up:** {prev.get('follow_up', 'Consult your doctor')}")
        else:
            st.write(wellness_plan.get('raw_plan', 'Unable to generate wellness plan'))

# TAB 4: Reports
with tab4:
    st.markdown('<div class="section-header"><h2>📊 Download Reports</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.analysis_done:
        st.warning("⚠️ Please complete symptom analysis first (Tab 1)")
    else:
        report_data = {
            'symptoms': st.session_state.symptoms,
            'risk_score': st.session_state.risk_score,
            'synthesis': st.session_state.synthesis,
            'evidence': st.session_state.evidence,
            'specialist_reports': st.session_state.agent_results
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📄 PDF Report")
            st.write("Comprehensive medical report")
            pdf_filename = f"health_report_{st.session_state.report_id}.pdf"
            try:
                ReportGenerator.generate_pdf(report_data, pdf_filename)
                with open(pdf_filename, "rb") as f:
                    st.download_button(
                        "📥 Download PDF",
                        data=f,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with col2:
            st.markdown("### 📋 JSON Report")
            st.write("Structured data export")
            json_filename = f"health_report_{st.session_state.report_id}.json"
            ReportGenerator.save_json(report_data, json_filename)
            with open(json_filename, "rb") as f:
                st.download_button(
                    "📥 Download JSON",
                    data=f,
                    file_name=json_filename,
                    mime="application/json",
                    use_container_width=True
                )
        
        with col3:
            st.markdown("### 📧 Email Report")
            st.write("Send to your email")
            email = st.text_input("Email address")
            if st.button("📧 Send Email", use_container_width=True):
                st.info("Email feature coming soon!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>⚠️ <strong>Medical Disclaimer:</strong> This AI system is for informational purposes only.</p>
    <p>It does not replace professional medical advice, diagnosis, or treatment.</p>
    <p>Always consult with qualified healthcare providers for medical decisions.</p>
    <p style='margin-top: 1rem; font-size: 0.9rem;'>© 2025 HealthAI Nexus | Powered by Groq AI</p>
</div>
""", unsafe_allow_html=True)
