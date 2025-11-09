import pytesseract
from PIL import Image
import PyPDF2
import io

def extract_text_from_image(image_file):
    """Extract text from image using OCR"""
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_file(uploaded_file):
    """Universal text extractor for images and PDFs"""
    file_type = uploaded_file.type if hasattr(uploaded_file, 'type') else uploaded_file.name.split('.')[-1]
    
    if 'pdf' in str(file_type).lower():
        return extract_text_from_pdf(uploaded_file)
    elif any(img_type in str(file_type).lower() for img_type in ['image', 'jpg', 'jpeg', 'png']):
        return extract_text_from_image(uploaded_file)
    else:
        # Try reading as text
        try:
            return uploaded_file.read().decode('utf-8')
        except:
            return "Unable to extract text from file"
