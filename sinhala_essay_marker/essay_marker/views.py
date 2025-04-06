from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from essay_marker.evaluator.word_count import calculate_word_count_marks
from essay_marker.evaluator.word_richness import calculate_word_richness_marks

@csrf_exempt
@require_POST
def evaluate_essay(request):
    try:
        data = json.loads(request.body)
        essay = data.get('essay', '')
        required_word_count = int(data.get('required_word_count', 0))
        topic = data.get('topic', '')  # Not used in current logic but available
        
        if not essay or required_word_count <= 0:
            return JsonResponse({'error': 'Invalid input'}, status=400)
        
        word_count_marks = calculate_word_count_marks(essay, required_word_count)
        word_richness_marks = calculate_word_richness_marks(essay)
        total_marks = round(word_count_marks + word_richness_marks, 2)
        
        return JsonResponse({
            'word_count_marks': word_count_marks,
            'word_richness_marks': word_richness_marks,
            'total_marks': total_marks
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)