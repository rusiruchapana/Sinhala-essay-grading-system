import re
import os
from docx import Document
from django.conf import settings

class SpellingEvaluator:
    def __init__(self):
        self.dictionary = self.load_dictionary()
    
    def preprocess_text(self, text):
        """Preprocess text keeping only Sinhala characters and spaces"""
        text = re.sub(r'[^\u0D80-\u0DFF\s]', '', text)
        return text.strip().lower()
    
    def tokenize(self, text):
        """Split text into words"""
        return text.split()
    
    def load_dictionary(self):
        """Load Sinhala dictionary from file"""
        dict_path = 'data\sinhala_dictionary.txt';
        try:
            with open(dict_path, 'r', encoding='utf-8') as f:
                return set(f.read().splitlines())
        except FileNotFoundError:
            raise Exception("Sinhala dictionary file not found. Please ensure the dictionary exists at the specified path.")
    
    def evaluate_spelling(self, text):
        """
        Evaluate spelling and return marks (out of 100)
        Returns:
        - spelling_marks (float)
        - misspelled_words (list)
        - total_words (int)
        """
        if not text:
            return 0.0, [], 0
        
        clean_text = self.preprocess_text(text)
        words = self.tokenize(clean_text)
        total_words = len(words)
        
        if total_words == 0:
            return 0.0, [], 0
        
        misspelled = [word for word in words if word not in self.dictionary]
        correct_words = total_words - len(misspelled)
        spelling_marks = (correct_words / total_words) * 100
        
        return spelling_marks, misspelled, total_words