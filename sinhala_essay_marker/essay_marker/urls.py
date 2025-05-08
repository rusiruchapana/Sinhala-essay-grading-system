from django.urls import path
from .views import evaluate_essay
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('evaluate-essay/', evaluate_essay, name='evaluate_essay'),
    
]