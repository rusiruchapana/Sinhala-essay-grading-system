# essays/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Essay
from .serializers import EssaySerializer
from .marks_give.word_count_marks import calculate_word_count_marks  # Import word count marks function
from .marks_give.richness_marks import calculate_richness_marks  # Import richness marks function

class EvaluateEssayView(APIView):
    def post(self, request):
        # Extract data from the request
        content = request.data.get('content', '')
        required_word_count = request.data.get('required_word_count', 0)
        topic = request.data.get('topic', '')

        # Calculate word count
        word_count = len(content.split())

        # Calculate marks using functions from the marks_give folder
        word_count_marks = calculate_word_count_marks(word_count, required_word_count)
        richness_marks = calculate_richness_marks(content)

        # Save the essay and its evaluation
        essay = Essay.objects.create(
            content=content,
            required_word_count=required_word_count,
            topic=topic,
            word_count=word_count,
            richness_score=richness_marks / 50,  # Store richness score (ratio)
            word_count_marks=word_count_marks,
            richness_marks=richness_marks
        )

        # Serialize the essay for response
        serializer = EssaySerializer(essay)
        return Response(serializer.data, status=status.HTTP_201_CREATED)