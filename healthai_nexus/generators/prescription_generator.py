import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

load_dotenv()

class PrescriptionGenerator:
    """Generate AI-powered medical prescriptions"""
    
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.2,
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def generate_prescription(self, patient_info, diagnosis, treatment_plan):
        """Generate detailed prescription"""
        prompt = f"""You are a licensed medical doctor. Generate a professional medical prescription.

PATIENT INFORMATION:
- Name: {patient_info['username']}
- Age: {patient_info['age']} years | Gender: Not specified
- Weight: {patient_info['weight']} kg ({patient_info.get('weight_lbs', 0):.0f} lbs)
- Height: {patient_info['height']} cm ({patient_info.get('height_ft', 'N/A')})
- BMI: {patient_info['bmi']:.1f} ({patient_info['bmi_category']})
- Allergies: {', '.join(patient_info['allergies']) if patient_info['allergies'] else 'None reported'}
- Current Medications: {', '.join(patient_info['current_medications']) if patient_info['current_medications'] else 'None'}

DIAGNOSIS:
{diagnosis}

CREATE A PROFESSIONAL PRESCRIPTION WITH:

1. Rx (Medications) - List each medication with:
   - Generic name (Brand name)
   - Strength/Dosage
   - Route (Oral/Topical/etc)
   - Frequency (e.g., 1 tablet twice daily)
   - Duration (e.g., for 7 days)
   - Special instructions (e.g., take with food)

2. INVESTIGATIONS (if needed):
   - Lab tests recommended
   - Imaging studies

3. ADVICE:
   - Dietary recommendations
   - Activity restrictions
   - Warning signs to watch for

4. FOLLOW-UP:
   - When to return
   - What to monitor

Format professionally like a real doctor's prescription."""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except:
            return "Unable to generate prescription. Please consult healthcare provider."
    
    def create_prescription_pdf(self, patient_info, prescription_text, filename):
        """Create prescription PDF with disclaimer"""
        doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        current_date = datetime.now()
        
        # DISCLAIMER AT TOP
        disclaimer_top_style = ParagraphStyle(
            'DisclaimerTop',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.red,
            borderColor=colors.red,
            borderWidth=2,
            borderPadding=8,
            backColor=colors.HexColor('#ffe6e6'),
            alignment=1
        )
        
        disclaimer_top = """<b>⚠️ IMPORTANT MEDICAL DISCLAIMER ⚠️</b><br/>
        This is an AI-GENERATED prescription for INFORMATIONAL PURPOSES ONLY.<br/>
        NOT A VALID LEGAL PRESCRIPTION. NOT A SUBSTITUTE FOR PROFESSIONAL MEDICAL ADVICE.<br/>
        ALWAYS CONSULT A LICENSED HEALTHCARE PROVIDER BEFORE TAKING ANY MEDICATION."""
        
        story.append(Paragraph(disclaimer_top, disclaimer_top_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Header
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=10,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph("🏥 MEDICAL PRESCRIPTION", header_style))
        
        subheader_style = ParagraphStyle(
            'SubHeader',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            alignment=1,
            spaceAfter=15
        )
        story.append(Paragraph("HealthAI Nexus - AI-Powered Healthcare Assistant", subheader_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Date and Prescription Number
        date_style = ParagraphStyle('DateStyle', parent=styles['Normal'], fontSize=10, spaceAfter=5)
        story.append(Paragraph(f"<b>Date of Issue:</b> {current_date.strftime('%B %d, %Y')}", date_style))
        story.append(Paragraph(f"<b>Time:</b> {current_date.strftime('%I:%M %p')}", date_style))
        story.append(Paragraph(f"<b>Prescription No:</b> RX-{current_date.strftime('%Y%m%d')}-{patient_info.get('username', 'PATIENT')[:4].upper()}", date_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Patient Info
        patient_header = ParagraphStyle('PatientHeader', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1f77b4'), spaceAfter=10, fontName='Helvetica-Bold')
        story.append(Paragraph("PATIENT INFORMATION", patient_header))
        
        patient_data = [
            ['Patient Name:', patient_info['username'].upper()],
            ['Age / Gender:', f"{patient_info['age']} years / Not specified"],
            ['Weight:', f"{patient_info['weight']} kg ({patient_info.get('weight_lbs', 0):.0f} lbs)"],
            ['Height:', f"{patient_info['height']} cm ({patient_info.get('height_ft', 'N/A')})"],
            ['BMI:', f"{patient_info['bmi']:.1f} ({patient_info['bmi_category']})"],
            ['Allergies:', ', '.join(patient_info['allergies']) if patient_info['allergies'] else 'None reported'],
            ['Current Medications:', ', '.join(patient_info['current_medications']) if patient_info['current_medications'] else 'None']
        ]
        
        patient_table = Table(patient_data, colWidths=[2*inch, 4.5*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1f77b4'))
        ]))
        story.append(patient_table)
        story.append(Spacer(1, 0.25*inch))
        
        # Prescription
        rx_header = ParagraphStyle('RxHeader', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1f77b4'), spaceAfter=10, fontName='Helvetica-Bold')
        story.append(Paragraph("℞ PRESCRIPTION", rx_header))
        
        prescription_style = ParagraphStyle('PrescriptionStyle', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=5)
        for line in prescription_text.split('\n'):
            if line.strip():
                story.append(Paragraph(line, prescription_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Important Notes
        note_style = ParagraphStyle('NoteStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#666666'), borderColor=colors.HexColor('#1f77b4'), borderWidth=1, borderPadding=8, backColor=colors.HexColor('#f5f5f5'))
        story.append(Paragraph("<b>IMPORTANT NOTES:</b>", styles['Heading3']))
        story.append(Paragraph(
            "• Take medications exactly as prescribed<br/>"
            "• Do not skip doses or stop medication without consulting doctor<br/>"
            "• Report any adverse reactions immediately<br/>"
            "• Keep all follow-up appointments<br/>"
            "• Store medications as directed",
            note_style
        ))
        story.append(Spacer(1, 0.2*inch))
        
        # Signature
        sig_style = ParagraphStyle('SigStyle', parent=styles['Normal'], fontSize=9, alignment=2)
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("_________________________", sig_style))
        story.append(Paragraph("<b>AI-Generated Prescription</b>", sig_style))
        story.append(Paragraph("HealthAI Nexus System", sig_style))
        story.append(Paragraph(f"Generated: {current_date.strftime('%Y-%m-%d %H:%M:%S')}", sig_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Bottom Disclaimer
        disclaimer_bottom_style = ParagraphStyle('DisclaimerBottom', parent=styles['Normal'], fontSize=7, textColor=colors.red, borderColor=colors.red, borderWidth=2, borderPadding=10, backColor=colors.HexColor('#fff3cd'), leading=10)
        
        disclaimer_bottom = """<b>⚠️ COMPREHENSIVE MEDICAL DISCLAIMER ⚠️</b><br/><br/>
        <b>THIS IS AN AI-GENERATED PRESCRIPTION FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY.</b><br/><br/>
        
        <b>NOT A VALID LEGAL PRESCRIPTION:</b> This document does not constitute a valid medical prescription 
        and cannot be used to obtain medications from pharmacies.<br/><br/>
        
        <b>NOT MEDICAL ADVICE:</b> This does not replace professional medical advice, diagnosis, or treatment 
        from a qualified, licensed healthcare provider.<br/><br/>
        
        <b>CONSULT A DOCTOR:</b> Always consult with a licensed physician, pharmacist, or other qualified 
        healthcare professional before starting, stopping, or changing any medication or treatment.<br/><br/>
        
        <b>NO DOCTOR-PATIENT RELATIONSHIP:</b> Use of this AI system does not create a doctor-patient relationship.<br/><br/>
        
        <b>EMERGENCY:</b> In case of medical emergency, call emergency services immediately (911 in US).<br/><br/>
        
        <b>LIABILITY:</b> HealthAI Nexus and its creators assume no liability for any actions taken based on 
        this AI-generated information. Use at your own risk.<br/><br/>
        
        <b>VERIFICATION REQUIRED:</b> All medical information should be verified with qualified healthcare professionals."""
        
        story.append(Paragraph(disclaimer_bottom, disclaimer_bottom_style))
        
        # Footer
        footer_style = ParagraphStyle('FooterStyle', parent=styles['Normal'], fontSize=7, textColor=colors.grey, alignment=1)
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            f"Generated by HealthAI Nexus | {current_date.strftime('%B %d, %Y at %I:%M %p')} | "
            f"Prescription ID: RX-{current_date.strftime('%Y%m%d%H%M%S')}",
            footer_style
        ))
        
        doc.build(story)
        return filename
