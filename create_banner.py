"""
Simple script to create project banner for GitHub
Run: python create_banner.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_banner():
    # Dimensions
    width, height = 1200, 600
    
    # Create image with gradient background
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Create purple to blue gradient
    for y in range(height):
        # Interpolate between purple (#667eea) and dark purple (#764ba2)
        r = int(102 + (118 - 102) * y / height)
        g = int(126 + (75 - 126) * y / height)
        b = int(234 + (162 - 234) * y / height)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
    
    # Try to load fonts, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 70)
        subtitle_font = ImageFont.truetype("arial.ttf", 30)
        feature_font = ImageFont.truetype("arial.ttf", 22)
        tech_font = ImageFont.truetype("arial.ttf", 18)
    except:
        print("⚠️ Arial font not found, using default font")
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        feature_font = ImageFont.load_default()
        tech_font = ImageFont.load_default()
    
    # Draw title
    draw.text((80, 120), "🏥 HealthAI Nexus", fill='white', font=title_font)
    
    # Draw subtitle
    draw.text((80, 210), "AI-Powered Multi-Agent Healthcare Assistant", 
              fill='white', font=subtitle_font)
    
    # Draw tagline
    draw.text((80, 260), "Transform healthcare with intelligent AI diagnosis", 
              fill=(255, 255, 255, 230), font=feature_font)
    
    # Draw features (right side)
    features = [
        "🩺 Multi-Agent Diagnosis",
        "💊 Smart Treatment Plans",
        "🌱 Wellness & Prevention",
        "📊 Interactive Dashboard",
        "📄 AI Prescriptions"
    ]
    
    y_pos = 120
    for feature in features:
        draw.text((700, y_pos), feature, fill='white', font=feature_font)
        y_pos += 70
    
    # Draw tech stack at bottom
    tech_text = "Python • Streamlit • Groq • Plotly • LangChain"
    draw.text((width//2 - 250, 540), tech_text, 
              fill=(255, 255, 255, 200), font=tech_font)
    
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Save image
    output_path = 'assets/banner.png'
    image.save(output_path, 'PNG', quality=95)
    
    print(f"Banner created successfully: {output_path}")
    print(f"Size: {width}x{height} px")
    print(f"Location: {os.path.abspath(output_path)}")
    print("\nNext steps:")
    print("1. Upload to GitHub: git add assets/banner.png")
    print("2. Commit: git commit -m 'Add project banner'")
    print("3. Push: git push origin main")

if __name__ == "__main__":
    try:
        create_banner()
    except Exception as e:
        print(f"Error creating banner: {e}")
        print("\nMake sure Pillow is installed: pip install pillow")
