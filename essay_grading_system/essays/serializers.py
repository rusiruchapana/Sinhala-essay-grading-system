from rest_framework import serializers
from .models import Essay

class EssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = [
            'id', 'content', 'required_word_count', 'topic',
            'word_count', 'richness_score', 'word_count_marks', 'richness_marks', 'created_at'
        ]
