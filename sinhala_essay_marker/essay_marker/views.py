from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import numpy as np
from .utils import is_sinhala
from essay_marker.file_processing.docx_extractor import process_uploaded_file
from essay_marker.evaluator.word_count import calculate_word_count_marks
from essay_marker.evaluator.word_richness import calculate_word_richness_marks
from essay_marker.evaluator.relevance_checker import calculate_relevance_marks
from essay_marker.evaluator.spelling_evaluator import SpellingEvaluator
from essay_marker.evaluator.grammar_evaluator import GrammarEvaluator
from .models import GradedEssay
from django.views.decorators.http import require_GET
from django.core import serializers
from django.views.decorators.http import require_http_methods


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
                return JsonResponse(
                    {'error': 'Only .docx files are supported'}, 
                    status=400
                )
            
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
                return JsonResponse(
                    {'error': 'Invalid JSON input'}, 
                    status=400
                )
        
        # Validate inputs
        if not essay:
            return JsonResponse(
                {'error': 'Essay text is required'}, 
                status=400
            )
        if required_word_count <= 0:
            return JsonResponse(
                {'error': 'Word count must be positive'}, 
                status=400
            )
        if not topic:
            return JsonResponse(
                {'error': 'Topic is required'}, 
                status=400
            )
        
        # Check if essay is in Sinhala
        is_sinhala_essay, sinhala_ratio = is_sinhala(essay)
        if not is_sinhala_essay:
            return JsonResponse(
                {
                    'error': 'Only Sinhala essays are accepted',
                    'details': ''
                }, 
                status=400
            )
        
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
        grammar_marks = grammar_evaluator.evaluate_grammar(essay)
        
        # Calculate total marks with weights
        total_marks = round(
            (word_count_marks * 0.15 + 
             word_richness_marks * 0.15 + 
             relevance_marks * 0.25 +
             convert_to_serializable(spelling_marks) * 0.25 +
             convert_to_serializable(grammar_marks) * 0.20),
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
        return JsonResponse(
            {'error': 'An unexpected error occurred', 'details': str(e)},
            status=500
        )

@csrf_exempt
@require_GET
def get_all_essays(request):
    try:
        essays = GradedEssay.objects.all().order_by('-created_at')
        essays_data = []
        
        for essay in essays:
            essays_data.append({
                'id': essay.id,
                'topic': essay.topic,
                'word_count': essay.word_count,
                'required_word_count': essay.required_word_count,
                'word_count_marks': essay.word_count_marks,
                'word_richness_marks': essay.word_richness_marks,
                'relevance_marks': essay.relevance_marks,
                'spelling_marks': essay.spelling_marks,
                'grammar_marks': essay.grammar_marks,
                'total_marks': essay.total_marks,
                'created_at': essay.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'essay_text': essay.essay_text[:100] + '...'  # First 100 chars
            })
            
        return JsonResponse({'essays': essays_data}, status=200)
        
    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to fetch essays', 'details': str(e)},
            status=500
        )
    
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_essay(request, essay_id):
    try:
        essay = GradedEssay.objects.get(id=essay_id)
        essay.delete()
        return JsonResponse({
            'success': True,
            'message': f'Essay with ID {essay_id} was deleted successfully'
        }, status=200)
    except GradedEssay.DoesNotExist:
        return JsonResponse(
            {'error': f'Essay with ID {essay_id} not found'},
            status=404
        )
    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to delete essay', 'details': str(e)},
            status=500
        )

