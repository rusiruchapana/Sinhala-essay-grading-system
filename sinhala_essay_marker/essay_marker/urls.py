from django.urls import path
from .views import evaluate_essay

urlpatterns = [
    path('evaluate-essay/', evaluate_essay, name='evaluate_essay'),
]