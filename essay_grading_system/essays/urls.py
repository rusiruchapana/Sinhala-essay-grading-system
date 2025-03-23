from django.urls import path
from .views import EvaluateEssayView

urlpatterns = [
    path('evaluate/', EvaluateEssayView.as_view(), name='evaluate_essay'),
]