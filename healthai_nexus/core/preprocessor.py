import re

class InputPreprocessor:
    """Cleans and redacts PHI from user input"""
    
    @staticmethod
    def clean_text(text):
        """Basic text cleaning"""
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text
    
    @staticmethod
    def redact_phi(text):
        """Redact common PHI patterns"""
        # Email
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        # Phone
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        # SSN
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
        return text
    
    @staticmethod
    def process(text):
        """Main preprocessing pipeline"""
        if not text:
            return ""
        text = InputPreprocessor.clean_text(text)
        text = InputPreprocessor.redact_phi(text)
        return text
