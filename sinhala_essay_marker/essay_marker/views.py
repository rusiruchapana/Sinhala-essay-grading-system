from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import numpy as np

from essay_marker.evaluator.word_count import calculate_word_count_marks
from essay_marker.evaluator.word_richness import calculate_word_richness_marks
from essay_marker.evaluator.relevance_checker import calculate_relevance_marks

def convert_to_serializable(value):
    """Convert numpy and other non-serializable types to native Python types"""
    if isinstance(value, (np.generic, np.ndarray)):
        return float(value)
    return value

@csrf_exempt
@require_POST
def evaluate_essay(request):
    try:
        data = json.loads(request.body)
        essay = data.get('essay', '')
        required_word_count = int(data.get('required_word_count', 0))
        topic = data.get('topic', '')
        
        if not essay or required_word_count <= 0 or not topic:
            return JsonResponse({'error': 'Invalid input'}, status=400)
        
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
        
        # Calculate total (average of all components)
        total_marks = round(
            (word_count_marks + word_richness_marks + relevance_marks) / 3, 
            2
        )
        
        return JsonResponse({
            'word_count_marks': word_count_marks,
            'word_richness_marks': word_richness_marks,
            'relevance_marks': relevance_marks,
            'total_marks': convert_to_serializable(total_marks)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)