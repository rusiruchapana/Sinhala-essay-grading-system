from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import numpy as np

from essay_marker.file_processing.docx_extractor import process_uploaded_file
from essay_marker.evaluator.word_count import calculate_word_count_marks
from essay_marker.evaluator.word_richness import calculate_word_richness_marks
from essay_marker.evaluator.relevance_checker import calculate_relevance_marks
from essay_marker.evaluator.spelling_evaluator import SpellingEvaluator

def convert_to_serializable(value):
    """Convert numpy and other non-serializable types to native Python types"""
    if isinstance(value, (np.generic, np.ndarray)):
        return float(value)
    return value

@csrf_exempt
@require_POST
def evaluate_essay(request):
    try:
        # Initialize spelling evaluator
        spelling_evaluator = SpellingEvaluator()
        
        # Initialize variables
        essay = ''
        required_word_count = 0
        topic = ''
        
        # Check if file was uploaded via form-data
        if request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            
            # Validate file extension
            if not uploaded_file.name.lower().endswith('.docx'):
                return HttpResponseBadRequest("Only .docx files are supported")
            
            # Process the uploaded file
            essay = process_uploaded_file(uploaded_file)
            
            # Get other parameters from form data
            required_word_count = int(request.POST.get('required_word_count', 0))
            topic = request.POST.get('topic', '')
        else:
            # Handle JSON input
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
        
        # Calculate all marks
        word_count_marks = convert_to_serializable(
            calculate_word_count_marks(essay, required_word_count)
        )
        word_richness_marks = convert_to_serializable(
            calculate_word_richness_marks(essay)
        )
        relevance_marks = convert_to_serializable(
            calculate_relevance_marks(essay, topic)
        )
        spelling_marks, _, _ = spelling_evaluator.evaluate_spelling(essay)
        
        # Calculate total marks (weighted average)
        total_marks = round(
            (word_count_marks * 0.2 + 
             word_richness_marks * 0.2 + 
             relevance_marks * 0.3 +
             convert_to_serializable(spelling_marks) * 0.3),
            2
        )
        
        return JsonResponse({
            'word_count_marks': word_count_marks,
            'word_richness_marks': word_richness_marks,
            'relevance_marks': relevance_marks,
            'spelling_marks': convert_to_serializable(spelling_marks),
            'total_marks': total_marks
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)