# HealthAI Nexus Dashboard - User Guide

## 🚀 New Features

### ✨ What's New in Dashboard Version

1. **🔐 Login/Register System**
   - Secure user authentication
   - Personal account management
   - User-specific data storage

2. **📊 Interactive Dashboard**
   - Visual health metrics
   - Risk score trends (line chart)
   - Risk distribution (pie chart)
   - Recent reports table

3. **👤 Enhanced Patient Profile**
   - Numeric input for Age (1-120 years)
   - Numeric input for Weight (kg)
   - Numeric input for Height (cm)
   - Auto-calculated BMI
   - Medical history tracking

4. **📄 AI-Generated Prescriptions**
   - Personalized prescription generation
   - Professional PDF format
   - Legal disclaimers included
   - Download functionality

5. **📈 Data Visualization**
   - Plotly interactive charts
   - Health trends over time
   - Risk category distribution
   - BMI tracking

6. **🗂️ Organized File Structure**
   - outputs/reports/ - Analysis reports
   - outputs/prescriptions/ - Prescription files
   - outputs/pdfs/ - PDF documents

---

## 🎯 How to Use

### Step 1: Login/Register

**First Time Users:**
1. Click "Register" tab
2. Enter username, email, password
3. Click "Register" button
4. Switch to "Login" tab

**Existing Users:**
1. Enter username and password
2. Click "Login" button

### Step 2: Update Personal Information

**In the left sidebar:**
- **Age:** Enter your age (e.g., 30)
- **Weight:** Enter weight in kg (e.g., 70.5)
- **Height:** Enter height in cm (e.g., 175.0)
- **BMI:** Automatically calculated
- **Allergies:** List any allergies (comma-separated)
- **Current Medications:** List medications you're taking
- **Existing Conditions:** List medical conditions

### Step 3: Dashboard Overview

**View your health metrics:**
- Total number of reports
- Average risk score
- Current BMI
- Age

**Interactive Charts:**
- **Risk Score Trend:** See how your risk changes over time
- **Risk Distribution:** View breakdown of low/medium/high risk reports
- **Recent Reports Table:** Quick access to past analyses

### Step 4: Symptom Analysis

1. Go to "🩺 Analysis" tab
2. Describe symptoms in detail
3. Upload medical reports (optional)
4. Click "🔍 Analyze Symptoms"
5. Wait 10-30 seconds
6. View results:
   - Risk score
   - Number of specialists consulted
   - Medical assessment

### Step 5: Treatment Plan

1. Go to "💊 Treatment" tab
2. View recommended medications
3. Check dosage and frequency
4. Review safety status
5. Note any warnings

### Step 6: Wellness Plan

1. Go to "🌱 Wellness" tab
2. View personalized diet recommendations
3. Check exercise routine
4. Review lifestyle modifications

### Step 7: Generate Prescription

1. Go to "📄 Prescription" tab
2. Click "Generate Prescription"
3. Review AI-generated prescription
4. Click "📥 Download Prescription PDF"
5. **READ THE DISCLAIMER CAREFULLY**

---

## 📊 Dashboard Features Explained

### Health Metrics Cards
- **Total Reports:** Number of analyses you've done
- **Avg Risk Score:** Your average health risk (0-10 scale)
- **BMI:** Body Mass Index (auto-calculated)
- **Age:** Your current age

### Risk Score Trend Chart
- **X-axis:** Date/time of analysis
- **Y-axis:** Risk score (0-10)
- **Purpose:** Track health changes over time
- **Interpretation:**
  - Downward trend = Improving health
  - Upward trend = Worsening symptoms
  - Flat line = Stable condition

### Risk Distribution Pie Chart
- **Green (Low):** Risk score 0-3
- **Yellow (Medium):** Risk score 4-6
- **Red (High):** Risk score 7-10
- **Purpose:** See overall health pattern

### Recent Reports Table
- **ID:** Report identification number
- **Timestamp:** When analysis was done
- **Symptoms:** Brief description
- **Risk Score:** Health risk level

---

## 🎨 UI Improvements

### Modern Design
- Gradient headers
- Card-based layout
- Smooth animations
- Responsive design

### Color Coding
- **Purple/Blue:** Primary actions
- **Green:** Safe/Low risk
- **Yellow:** Caution/Medium risk
- **Red:** Warning/High risk

### Interactive Elements
- Hover effects on buttons
- Expandable sections
- Collapsible cards
- Smooth transitions

---

## 📁 File Organization

### Automatic File Management

**Reports:**
```
outputs/reports/
  ├── health_report_1.json
  ├── health_report_2.json
  └── ...
```

**Prescriptions:**
```
outputs/prescriptions/
  ├── prescription_1.pdf
  ├── prescription_2.pdf
  └── ...
```

**PDFs:**
```
outputs/pdfs/
  ├── analysis_report_1.pdf
  ├── analysis_report_2.pdf
  └── ...
```

---

## 🔒 Security Features

### Password Protection
- Passwords are hashed (SHA-256)
- Never stored in plain text
- Secure authentication

### User Privacy
- Each user has separate data
- Reports linked to user accounts
- No data sharing between users

### Session Management
- Automatic logout option
- Session state tracking
- Secure user sessions

---

## ⚠️ Important Disclaimers

### AI-Generated Prescriptions
```
⚠️ CRITICAL DISCLAIMER:
This prescription is AI-generated for informational purposes only.
It does NOT constitute professional medical advice, diagnosis, or treatment.
This is NOT a valid legal prescription.
Always consult with a qualified, licensed healthcare provider.
Do not use this for self-medication.
```

### General Medical Advice
- This is an AI assistant, not a doctor
- Emergency symptoms require immediate medical care
- Always verify with healthcare professionals
- Keep patient information private

---

## 🎯 Best Practices

### For Accurate Analysis
1. **Be Specific:** Include duration, severity, location
2. **Update Profile:** Keep age, weight, height current
3. **List Medications:** Include all current medications
4. **Note Allergies:** List all known allergies
5. **Upload Reports:** Add lab results when available

### For Better Tracking
1. **Regular Check-ins:** Analyze symptoms periodically
2. **Monitor Trends:** Check dashboard charts weekly
3. **Save Reports:** Download important prescriptions
4. **Update Conditions:** Add new diagnoses

### For Safety
1. **Read Disclaimers:** Always read warnings
2. **Verify Medications:** Check with pharmacist
3. **Emergency Care:** Don't delay for serious symptoms
4. **Professional Advice:** Consult doctors for treatment

---

## 🚀 Quick Start Commands

### Run Dashboard Version
```bash
streamlit run healthai_nexus/app_dashboard.py
```

### Install New Dependencies
```bash
pip install plotly
```

### Access Application
```
http://localhost:8501
```

---

## 📊 Example Workflow

### Complete Health Check

1. **Login** to your account
2. **Update** personal information (age, weight, height)
3. **Enter** current symptoms
4. **Analyze** with AI doctors
5. **View** dashboard metrics
6. **Check** treatment recommendations
7. **Review** wellness plan
8. **Generate** prescription (if needed)
9. **Download** reports for records
10. **Track** progress over time

---

## 🆘 Troubleshooting

### Login Issues
- **Problem:** Can't login
- **Solution:** Check username/password, try registering again

### Chart Not Showing
- **Problem:** Dashboard charts empty
- **Solution:** Complete at least one symptom analysis

### Prescription Generation Fails
- **Problem:** Can't generate prescription
- **Solution:** Complete symptom analysis first

### BMI Shows Wrong Value
- **Problem:** BMI calculation incorrect
- **Solution:** Check weight (kg) and height (cm) units

---

## 📞 Support

For issues or questions:
1. Check this guide
2. Review QUICK_START.md
3. Run test scripts
4. Check API key in .env

---

## 🎉 Enjoy Your Enhanced Dashboard!

**Version:** 3.0 (Dashboard Edition)
**Last Updated:** 2025
**Features:** Login, Dashboard, Visualizations, Prescriptions

---

**Made with ❤️ using Groq AI + Streamlit + Plotly**
