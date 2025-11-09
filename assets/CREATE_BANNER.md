# Creating Project Banner/Thumbnail

## 🎨 Banner Specifications

**Dimensions:** 1200 x 600 px (GitHub social preview)  
**Format:** PNG or JPG  
**File Size:** < 1 MB

---

## 🚀 Quick Create with Canva (Recommended)

### Step 1: Go to Canva
Visit: https://www.canva.com/create/banners/

### Step 2: Create Custom Size
- Click "Custom size"
- Enter: 1200 x 600 px
- Click "Create new design"

### Step 3: Design Elements

#### Background
- **Gradient:** Purple (#667eea) to Blue (#764ba2)
- **Style:** Diagonal gradient (top-left to bottom-right)

#### Title Section (Left Side)
```
🏥 HealthAI Nexus
Font: Montserrat Bold, 72px, White
Position: 100px from left, 150px from top
```

#### Subtitle
```
AI-Powered Multi-Agent Healthcare Assistant
Font: Montserrat Regular, 32px, White
Position: Below title, 20px spacing
```

#### Feature Icons (Right Side)
```
🩺 Multi-Agent Diagnosis
💊 Smart Treatment Plans
🌱 Wellness & Prevention
📊 Interactive Dashboard
📄 AI Prescriptions

Font: Montserrat Medium, 20px, White
Position: Right side, vertically centered
Spacing: 30px between each
```

#### Tech Stack (Bottom)
```
Python | Streamlit | Groq | Plotly | LangChain

Font: Montserrat Regular, 18px, White (80% opacity)
Position: Bottom center, 30px from bottom
```

### Step 4: Download
- Click "Share" → "Download"
- Format: PNG
- Quality: High
- Download

### Step 5: Save
Save as: `banner.png` in the `assets/` folder

---

## 🎨 Alternative: Use Figma

### Template Design
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  🏥 HealthAI Nexus                    🩺 Multi-Agent       │
│  AI-Powered Healthcare Assistant      💊 Smart Treatment   │
│                                       🌱 Wellness Plans     │
│  Transform healthcare with AI         📊 Dashboard         │
│  • 11 Specialized Doctors             📄 Prescriptions     │
│  • Real-time Drug Safety                                   │
│  • Personalized Treatment                                  │
│                                                             │
│  Python | Streamlit | Groq | Plotly | LangChain           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🖼️ Screenshot Guide

### Dashboard Screenshot
1. Run the app: `python -m streamlit run healthai_nexus/app_dashboard.py`
2. Login and navigate to Dashboard tab
3. Take screenshot (Windows: Win+Shift+S)
4. Save as: `dashboard.png`

### Treatment Screenshot
1. Complete a symptom analysis
2. Go to Treatment tab
3. Take screenshot
4. Save as: `treatment.png`

### Wellness Screenshot
1. Go to Wellness tab
2. Take screenshot
3. Save as: `wellness.png`

### Prescription Screenshot
1. Generate a prescription
2. Take screenshot
3. Save as: `prescription.png`

---

## 📐 Image Sizes

| Image | Size | Purpose |
|-------|------|---------|
| banner.png | 1200 x 600 | Main banner |
| dashboard.png | 800 x 400 | Dashboard demo |
| treatment.png | 800 x 400 | Treatment demo |
| wellness.png | 800 x 400 | Wellness demo |
| prescription.png | 800 x 400 | Prescription demo |
| logo.png | 512 x 512 | Project logo |

---

## 🎨 Color Palette

```css
/* Primary Colors */
--purple: #667eea;
--dark-purple: #764ba2;
--blue: #1f77b4;

/* Status Colors */
--success: #28a745;
--warning: #ffc107;
--danger: #dc3545;
--info: #17a2b8;

/* Neutral */
--white: #ffffff;
--light-gray: #f8f9fa;
--dark-gray: #343a40;
```

---

## 🔧 Python Script to Create Banner

Save as `create_banner.py`:

```python
from PIL import Image, ImageDraw, ImageFont
import os

# Create image with gradient
width, height = 1200, 600
image = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(image)

# Create gradient
for y in range(height):
    r = int(102 + (118 - 102) * y / height)
    g = int(126 + (75 - 126) * y / height)
    b = int(234 + (162 - 234) * y / height)
    draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))

# Load fonts (use default if not available)
try:
    title_font = ImageFont.truetype("arial.ttf", 72)
    subtitle_font = ImageFont.truetype("arial.ttf", 32)
    feature_font = ImageFont.truetype("arial.ttf", 20)
    tech_font = ImageFont.truetype("arial.ttf", 18)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    feature_font = ImageFont.load_default()
    tech_font = ImageFont.load_default()

# Title
draw.text((100, 150), "🏥 HealthAI Nexus", fill='white', font=title_font)

# Subtitle
draw.text((100, 240), "AI-Powered Healthcare Assistant", fill='white', font=subtitle_font)

# Features (right side)
features = [
    "🩺 Multi-Agent Diagnosis",
    "💊 Smart Treatment Plans",
    "🌱 Wellness & Prevention",
    "📊 Interactive Dashboard",
    "📄 AI Prescriptions"
]

y_pos = 150
for feature in features:
    draw.text((700, y_pos), feature, fill='white', font=feature_font)
    y_pos += 70

# Tech stack
draw.text((300, 550), "Python | Streamlit | Groq | Plotly | LangChain", 
          fill=(255, 255, 255, 200), font=tech_font)

# Save
os.makedirs('assets', exist_ok=True)
image.save('assets/banner.png')
print("✅ Banner created: assets/banner.png")
```

Run:
```bash
pip install pillow
python create_banner.py
```

---

## 📤 Upload to GitHub

### Method 1: Direct Upload
1. Go to your GitHub repository
2. Click "Add file" → "Upload files"
3. Drag `assets/banner.png`
4. Commit changes

### Method 2: Git Command
```bash
git add assets/banner.png
git commit -m "Add project banner"
git push origin main
```

### Method 3: GitHub Social Preview
1. Go to repository Settings
2. Scroll to "Social preview"
3. Click "Edit"
4. Upload `banner.png` (1200 x 630 px)

---

## ✅ Checklist

- [ ] Create banner.png (1200 x 600)
- [ ] Take dashboard screenshot
- [ ] Take treatment screenshot
- [ ] Take wellness screenshot
- [ ] Take prescription screenshot
- [ ] Upload all to assets/ folder
- [ ] Update README.md image links
- [ ] Set GitHub social preview
- [ ] Test all image links

---

## 🎯 Final Result

Your README will display:
```markdown
![HealthAI Nexus Banner](https://raw.githubusercontent.com/yourusername/healthai-nexus/main/assets/banner.png)
```

**Note:** Replace `yourusername` with your actual GitHub username!

---

**Pro Tip:** Use high-quality images and maintain consistent branding throughout!
