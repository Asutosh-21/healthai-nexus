# HealthAI Nexus - Feature Demo

## 🎬 Demo Scenarios

### Scenario 1: Common Cold with Fever

#### Input:
```
Symptoms: "High fever (102°F), runny nose, sore throat, body aches, 
          cough for 3 days. Feeling very tired."

Patient Profile:
- Age: Adult (18-64)
- Weight: Normal
- Allergies: Penicillin
- Current Meds: None
- Conditions: None
```

#### Expected Output:

**🩺 Triage Routing:**
- ✅ General Practitioner
- ✅ Pharmacologist

**📊 Risk Score:** 3-4/10 (Low-Medium)

**💊 Treatment Plan:**
- Acetaminophen 500mg every 6 hours
- Dextromethorphan for cough
- Rest and hydration
- Safety: ✅ Safe (no penicillin)

**🌱 Wellness Plan:**
- Diet: Warm soups, citrus fruits, ginger tea
- Rest: 8-10 hours sleep
- Hydration: 10-12 glasses water
- Avoid: Dairy, cold foods

---

### Scenario 2: Chest Pain (Emergency)

#### Input:
```
Symptoms: "Severe chest pain radiating to left arm, shortness of breath,
          sweating, nausea. Started 30 minutes ago."

Patient Profile:
- Age: Senior (65+)
- Weight: Overweight
- Allergies: None
- Current Meds: Aspirin, Metformin
- Conditions: Diabetes, Hypertension
```

#### Expected Output:

**🩺 Triage Routing:**
- ✅ Cardiologist
- ✅ General Practitioner

**📊 Risk Score:** 9-10/10 (HIGH - EMERGENCY)

**⚠️ Urgent Alert:**
"SEEK IMMEDIATE EMERGENCY CARE - Possible cardiac event"

**💊 Treatment Plan:**
- Emergency: Call 911 immediately
- Chew aspirin 325mg (if not allergic)
- Hospital evaluation required
- ECG, Troponin tests needed

**🌱 Preventive (Post-Recovery):**
- Cardiac rehabilitation program
- Heart-healthy diet (low sodium, low fat)
- Stress management
- Regular cardiology follow-up

---

### Scenario 3: Diabetes Management

#### Input:
```
Symptoms: "Increased thirst, frequent urination, fatigue, blurred vision.
          Weight loss of 10 lbs in 2 months. Family history of diabetes."

Patient Profile:
- Age: Adult (18-64)
- Weight: Overweight
- Allergies: None
- Current Meds: None
- Conditions: Pre-diabetes
```

#### Expected Output:

**🩺 Triage Routing:**
- ✅ Nutritionist
- ✅ Pharmacologist
- ✅ General Practitioner

**📊 Risk Score:** 6-7/10 (Medium-High)

**💊 Treatment Plan:**
- Metformin 500mg twice daily
- Blood glucose monitoring
- HbA1c test every 3 months
- Endocrinology referral

**🌱 Wellness Plan:**

**Diet:**
- Low glycemic index foods
- Avoid: Sugar, refined carbs, processed foods
- Eat: Whole grains, vegetables, lean protein
- Portion control

**Exercise:**
- 30 minutes daily walking
- Resistance training 2x/week
- Monitor blood sugar before/after

**Lifestyle:**
- Weight loss goal: 5-10% body weight
- Sleep: 7-8 hours
- Stress reduction: Meditation, yoga

**Preventive:**
- Eye exam annually
- Foot check daily
- Kidney function tests
- Dental checkups

---

### Scenario 4: Skin Rash

#### Input:
```
Symptoms: "Red itchy rash on arms and legs for 1 week. 
          Started after using new laundry detergent."

Patient Profile:
- Age: Adult (18-64)
- Weight: Normal
- Allergies: Latex
- Current Meds: None
- Conditions: Eczema history
```

#### Expected Output:

**🩺 Triage Routing:**
- ✅ Dermatologist
- ✅ Pharmacologist

**📊 Risk Score:** 2/10 (Low)

**💊 Treatment Plan:**
- Hydrocortisone cream 1% twice daily
- Oral antihistamine (Cetirizine 10mg)
- Avoid irritant (change detergent)
- Moisturize regularly

**🌱 Wellness Plan:**
- Use fragrance-free products
- Wear cotton clothing
- Avoid hot showers
- Keep skin moisturized
- Identify and avoid triggers

---

### Scenario 5: Insomnia & Stress

#### Input:
```
Symptoms: "Can't fall asleep, waking up multiple times at night.
          Feeling anxious and stressed. Work pressure high.
          Tired during day but can't sleep at night."

Patient Profile:
- Age: Adult (18-64)
- Weight: Normal
- Allergies: None
- Current Meds: None
- Conditions: None
```

#### Expected Output:

**🩺 Triage Routing:**
- ✅ Sleep Specialist
- ✅ General Practitioner

**📊 Risk Score:** 4/10 (Medium)

**💊 Treatment Plan:**
- Melatonin 3mg before bed
- Avoid: Caffeine after 2 PM
- Consider: Cognitive Behavioral Therapy for Insomnia (CBT-I)
- Short-term: Low-dose sleep aid if needed

**🌱 Wellness Plan:**

**Sleep Hygiene:**
- Consistent sleep schedule (10 PM - 6 AM)
- Dark, cool bedroom (65-68°F)
- No screens 1 hour before bed
- Relaxing bedtime routine

**Stress Management:**
- Deep breathing exercises
- Progressive muscle relaxation
- Meditation 10 minutes daily
- Journaling before bed

**Lifestyle:**
- Exercise: Morning or afternoon (not evening)
- Limit alcohol
- Light dinner 3 hours before bed
- Warm bath before sleep

**Preventive:**
- Stress management workshop
- Work-life balance assessment
- Regular exercise routine
- Social support network

---

## 🎯 Key Features Demonstrated

### ✅ Intelligent Triage
- Routes to appropriate specialists
- Handles emergency vs routine cases
- Considers symptom severity

### ✅ Personalized Treatment
- Age-appropriate recommendations
- Considers allergies and current medications
- Drug interaction checking
- Dosage based on patient profile

### ✅ Drug Safety
- Allergy validation
- Interaction warnings
- Alternative suggestions
- OpenFDA verified information

### ✅ Comprehensive Wellness
- Personalized diet plans
- Exercise routines
- Lifestyle modifications
- Preventive measures

### ✅ Risk Assessment
- 0-10 scale scoring
- Urgency indicators
- Emergency alerts
- Follow-up recommendations

### ✅ Professional UI
- Organized tabs
- Patient profile management
- Progress tracking
- Downloadable reports

---

## 🚀 Try It Yourself

1. **Start the app:**
   ```bash
   streamlit run healthai_nexus/app_enhanced.py
   ```

2. **Enter patient profile** in sidebar

3. **Choose a scenario** from above

4. **Navigate through tabs:**
   - Tab 1: See analysis
   - Tab 2: View treatment plan
   - Tab 3: Get wellness recommendations
   - Tab 4: Download reports

5. **Experiment with different symptoms!**

---

## 📊 Performance Metrics

- **Analysis Time:** 10-30 seconds
- **Specialists Consulted:** 2-4 per case
- **Accuracy:** Based on Groq LLM (llama-3.3-70b)
- **Safety Checks:** Real-time validation
- **Report Generation:** < 5 seconds

---

## ⚠️ Important Reminders

- This is an AI assistant, not a doctor
- Emergency symptoms require immediate medical care
- Always verify recommendations with healthcare providers
- Keep patient information private and secure
- Use for informational purposes only

---

**Ready to revolutionize healthcare with AI? Let's go! 🚀**
