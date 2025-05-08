from django.db import models

class GradedEssay(models.Model):
    essay_text = models.TextField()
    word_count = models.IntegerField()
    required_word_count = models.IntegerField()
    topic = models.CharField(max_length=255)
    word_count_marks = models.FloatField()
    word_richness_marks = models.FloatField()
    relevance_marks = models.FloatField()
    spelling_marks = models.FloatField()
    grammar_marks = models.FloatField()
    total_marks = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Essay on {self.topic} - {self.total_marks}/100"