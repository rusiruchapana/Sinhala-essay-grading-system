from django.urls import path
from .views import evaluate_essay, get_all_essays, delete_essay

urlpatterns = [
    path('evaluate-essay/', evaluate_essay, name='evaluate_essay'),
    path('get-all-essays/', get_all_essays, name='get_all_essays'),  # Add this line
    path('delete-essay/<int:essay_id>/', delete_essay, name='delete_essay'),
]