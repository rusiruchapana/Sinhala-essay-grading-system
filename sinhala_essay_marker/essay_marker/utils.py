import re

def is_sinhala(text, threshold=0.7):
    """
    Check if text is primarily Sinhala by character composition
    threshold: minimum ratio of Sinhala characters (0-1)
    """
    if not text.strip():
        return False
        
    # Count Sinhala characters (Unicode range for Sinhala)
    sinhala_chars = re.findall(r'[\u0D80-\u0DFF]', text)
    total_chars = len([c for c in text if not c.isspace()])
    
    if total_chars == 0:
        return False
        
    ratio = len(sinhala_chars) / total_chars
    return ratio >= threshold