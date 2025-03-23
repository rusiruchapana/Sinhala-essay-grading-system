from django.db import models

class Essay(models.Model):
    content = models.TextField()  # To store the essay content
    required_word_count = models.IntegerField(default=0)  # Default value is 0
    topic = models.CharField(max_length=255, default="")  # Default value is an empty string
    word_count = models.IntegerField(default=0)  # Actual word count
    richness_score = models.FloatField(default=0.0)  # Richness score
    word_count_marks = models.FloatField(default=0.0)  # Marks for word count
    richness_marks = models.FloatField(default=0.0)  # Marks for richness
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Essay {self.id}"