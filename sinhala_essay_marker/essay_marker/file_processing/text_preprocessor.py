import re

class SinhalaTextPreprocessor:
    """Preprocess Sinhala text for evaluation"""
    
    def __init__(self):
        # Pre-compile regex patterns for better performance
        self.non_sinhala_pattern = re.compile(r'[^\u0D80-\u0DFF\s.,!?;:\'"()-]')
        self.whitespace_pattern = re.compile(r'\s+')
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize Sinhala text"""
        text = self.non_sinhala_pattern.sub('', text)
        text = self.whitespace_pattern.sub(' ', text).strip()
        return text
    
    def extract_metadata(self, text: str) -> dict:
        """Extract potential metadata from text (if needed)"""
        # Could be enhanced to detect title, author, etc.
        return {
            'word_count': len(text.split()),
            'char_count': len(text)
        }