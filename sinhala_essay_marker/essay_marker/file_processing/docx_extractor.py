import os
import docx
import tempfile
from typing import Tuple

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a Word document"""
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text])
    except Exception as e:
        raise ValueError(f"Error reading Word file: {str(e)}")

def process_uploaded_file(uploaded_file) -> str:
    """Process uploaded file and extract essay text with proper temp file handling"""
    try:
        # Create a temporary file with a proper extension
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
            # Write the uploaded file in chunks to handle large files
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)
            tmp_path = tmp_file.name
        
        # Extract text
        raw_text = extract_text_from_docx(tmp_path)
        
        # Clean up the temporary file
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        
        return raw_text
    except Exception as e:
        # Ensure temporary file is deleted even if an error occurs
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        raise e