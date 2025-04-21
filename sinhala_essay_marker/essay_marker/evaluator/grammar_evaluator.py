from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
import math
from django.conf import settings
import os

class GrammarEvaluator:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GrammarEvaluator, cls).__new__(cls)
            cls._instance.initialize_model()
        return cls._instance
    
    def initialize_model(self):
        """Initialize model only once when first needed"""
        model_name = "xlm-roberta-base"
        model_path = os.path.join(settings.BASE_DIR, 'models', model_name)
        
        try:
            # Try to load locally cached model first
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForMaskedLM.from_pretrained(model_path)
        except:
            # Download and cache if not available locally
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForMaskedLM.from_pretrained(model_name)
            # Save for future use
            self.model.save_pretrained(model_path)
            self.tokenizer.save_pretrained(model_path)
            
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
    
    def calculate_perplexity(self, text):
        """Efficient perplexity calculation with batch processing"""
        if not text.strip():
            return 0.0
            
        encodings = self.tokenizer(text, return_tensors='pt').to(self.device)
        input_ids = encodings['input_ids'][0]
        
        if len(input_ids) <= 2:  # Too short for meaningful evaluation
            return 100.0  # High perplexity for very short texts
            
        with torch.no_grad():
            outputs = self.model(input_ids.unsqueeze(0))
            logits = outputs.logits
            
        losses = []
        for i in range(1, len(input_ids) - 1):  # Skip special tokens
            log_prob = torch.nn.functional.log_softmax(logits[0, i], dim=-1)
            loss = -log_prob[input_ids[i]].item()
            losses.append(loss)
        
        avg_loss = sum(losses) / len(losses) if losses else 0
        return math.exp(avg_loss)
    
    def evaluate_grammar(self, text):
        """
        Evaluate grammar quality based on perplexity
        Returns marks out of 100 (higher is better)
        """
        perplexity = self.calculate_perplexity(text)
        
        # Normalize score (adjust these thresholds as needed)
        if perplexity < 10:
            score = 90 + (10 - perplexity)
        elif perplexity < 20:
            score = 80 + (20 - perplexity) * 0.5
        elif perplexity < 40:
            score = 60 + (40 - perplexity) * 0.5
        else:
            score = max(40 - (perplexity - 40) * 0.5, 0)
            
        return round(min(score, 100), 2)