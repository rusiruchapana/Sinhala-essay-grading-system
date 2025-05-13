from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import numpy as np
from .utils import is_sinhala  # Add this import
from essay_marker.file_processing.docx_extractor import process_uploaded_file
from essay_marker.evaluator.word_count import calculate_word_count_marks
from essay_marker.evaluator.word_richness import calculate_word_richness_marks
from essay_marker.evaluator.relevance_checker import calculate_relevance_marks
from essay_marker.evaluator.spelling_evaluator import SpellingEvaluator
from essay_marker.evaluator.grammar_evaluator import GrammarEvaluator
from .models import GradedEssay

def convert_to_serializable(value):
    """Convert numpy and other non-serializable types to native Python types"""
    if isinstance(value, (np.generic, np.ndarray)):
        return float(value)
    return value

@csrf_exempt
@require_POST
def evaluate_essay(request):
    try:
        # Initialize evaluators
        spelling_evaluator = SpellingEvaluator()
        grammar_evaluator = GrammarEvaluator()
        
        # Initialize variables
        essay = ''
        required_word_count = 0
        topic = ''
        file_uploaded = False
        
        # Check if file was uploaded via form-data
        if request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            file_uploaded = True
            
            if not uploaded_file.name.lower().endswith('.docx'):
                return HttpResponseBadRequest("Only .docx files are supported")
            
            essay = process_uploaded_file(uploaded_file)
            required_word_count = int(request.POST.get('required_word_count', 0))
            topic = request.POST.get('topic', '')
        else:
            try:
                data = json.loads(request.body)
                essay = data.get('essay', '')
                required_word_count = int(data.get('required_word_count', 0))
                topic = data.get('topic', '')
            except json.JSONDecodeError:
                return HttpResponseBadRequest("Invalid JSON input")
        
        # Validate inputs
        if not essay:
            return HttpResponseBadRequest("Essay text is required")
        if required_word_count <= 0:
            return HttpResponseBadRequest("Word count must be positive")
        if not topic:
            return HttpResponseBadRequest("Topic is required")
        
        # Check if essay is in Sinhala (at least 70% Sinhala characters)
        if not is_sinhala(essay):
            return HttpResponseBadRequest("Only Sinhala essays are accepted. Please submit your essay in Sinhala.")
        
        # Calculate all marks
        word_count_marks = convert_to_serializable(
            calculate_word_count_marks(essay, required_word_count)
        )
        word_richness_marks = convert_to_serializable(
            calculate_word_richness_marks(essay))
        relevance_marks = convert_to_serializable(
            calculate_relevance_marks(essay, topic))
        spelling_marks, _, _ = spelling_evaluator.evaluate_spelling(essay)
        grammar_marks = grammar_evaluator.evaluate_grammar(essay)
        
        # Calculate total marks with weights
        total_marks = round(
            (word_count_marks * 0.10 + 
             word_richness_marks * 0.20 + 
             relevance_marks * 0.35 +
             convert_to_serializable(spelling_marks) * 0.10 +
             convert_to_serializable(grammar_marks) * 0.25),
            2
        )
        
        # Save to database
        GradedEssay.objects.create(
            essay_text=essay,
            word_count=len(essay.split()),
            required_word_count=required_word_count,
            topic=topic,
            word_count_marks=word_count_marks,
            word_richness_marks=word_richness_marks,
            relevance_marks=relevance_marks,
            spelling_marks=spelling_marks,
            grammar_marks=grammar_marks,
            total_marks=total_marks
        )
        
        return JsonResponse({
            'word_count_marks': word_count_marks,
            'word_richness_marks': word_richness_marks,
            'relevance_marks': relevance_marks,
            'spelling_marks': convert_to_serializable(spelling_marks),
            'grammar_marks': grammar_marks,
            'total_marks': total_marks
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)