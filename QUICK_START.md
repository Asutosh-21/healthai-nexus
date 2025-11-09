# HealthAI Nexus - Quick Start Guide

## 🚀 Installation

### 1. Install Dependencies
```bash
cd healthai_nexus
pip install -r requirements.txt
```

### 2. Set Up Environment
Create `.env` file in root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from: https://console.groq.com/

### 3. Run Application
```bash
# Enhanced version with all features
streamlit run healthai_nexus/app_enhanced.py

# Or basic version
streamlit run healthai_nexus/app_new.py
```

## 📱 Using the Application

### Step 1: Enter Patient Profile (Sidebar)
- Select age group
- Choose weight category
- Add allergies (comma-separated)
- List current medications
- Note existing conditions

### Step 2: Symptom Analysis (Tab 1)
1. Describe your symptoms in detail
2. Upload medical reports (optional)
3. Click "Analyze Symptoms"
4. View specialist consultations
5. Check risk score and evidence

### Step 3: Treatment Plan (Tab 2)
- View personalized medication recommendations
- Check drug safety status
- See dosage instructions
- Review non-pharmacological treatments
- Note monitoring requirements

### Step 4: Wellness Plan (Tab 3)
- Get personalized diet plan
- Follow exercise routine
- Implement lifestyle changes
- Schedule preventive screenings

### Step 5: Download Reports (Tab 4)
- Download PDF report
- Export JSON data
- Email report (coming soon)

## 🧪 Testing

### Test Triage System
```bash
python healthai_nexus/test_triage.py
```

### Test Enhanced Features
```bash
python healthai_nexus/test_enhanced_features.py
```

### Test Full System
```bash
python healthai_nexus/test_system.py
```

## 📋 Example Use Cases

### Case 1: Common Cold
**Symptoms:** "High fever, cough, sore throat, body aches"
**Expected:** Routes to General Practitioner + Pharmacologist
**Treatment:** OTC medications, rest, hydration
**Wellness:** Immune-boosting diet, adequate sleep

### Case 2: Chest Pain
**Symptoms:** "Chest pain, shortness of breath, sweating"
**Expected:** Routes to Cardiologist + General Practitioner
**Treatment:** Emergency evaluation, cardiac tests
**Wellness:** Heart-healthy diet, stress management

### Case 3: Chronic Condition
**Symptoms:** "Diabetes management, weight concerns"
**Expected:** Routes to Nutritionist + Pharmacologist
**Treatment:** Medication adjustment, glucose monitoring
**Wellness:** Diabetic diet plan, exercise routine

## 🔧 Troubleshooting

### Issue: API Key Error
**Solution:** Check `.env` file has correct GROQ_API_KEY

### Issue: Module Not Found
**Solution:** Run `pip install -r requirements.txt`

### Issue: Unicode Error
**Solution:** Set environment variable: `set PYTHONIOENCODING=utf-8`

### Issue: PDF Generation Error
**Solution:** Install reportlab: `pip install reportlab`

## 📊 Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| Multi-Agent Analysis | 8 specialist agents | ✅ |
| Intelligent Triage | Smart routing | ✅ |
| OCR/PDF Reading | File upload support | ✅ |
| RAG Evidence | Medical knowledge | ✅ |
| Risk Scoring | 0-10 scale | ✅ |
| Treatment Plans | Personalized meds | ✅ |
| Drug Safety | Interaction checking | ✅ |
| Wellness Plans | Diet/Exercise/Lifestyle | ✅ |
| PDF Reports | Downloadable | ✅ |
| JSON Export | Data portability | ✅ |
| Database | SQLite storage | ✅ |
| Patient Profile | Personalization | ✅ |

## 🎯 Best Practices

1. **Be Specific:** Provide detailed symptom descriptions
2. **Include Duration:** Mention how long symptoms have lasted
3. **Update Profile:** Keep patient profile current
4. **Upload Reports:** Add lab results for better analysis
5. **Follow Up:** Track progress with report history

## ⚠️ Important Notes

- This is an AI assistant, NOT a replacement for doctors
- Always consult healthcare professionals for medical decisions
- Emergency symptoms require immediate medical attention
- Keep your API key secure and private
- Review drug interactions with your pharmacist

## 🆘 Emergency Symptoms

Seek immediate medical care if you experience:
- Chest pain or pressure
- Difficulty breathing
- Severe bleeding
- Loss of consciousness
- Stroke symptoms (FAST)
- Severe allergic reactions

## 📞 Support

For issues or questions:
1. Check documentation in README.md
2. Review FEATURES_ADDED.md
3. Run test scripts to verify setup
4. Check Groq API status

## 🔄 Updates

Check for updates regularly:
- New specialist agents
- Enhanced drug database
- Improved wellness recommendations
- Additional API integrations

---

**Version:** 2.0
**Last Updated:** 2025
**License:** MIT
