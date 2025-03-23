# essays/marks_give/richness_marks.py

def calculate_richness_marks(content):
    """
    Calculate marks based on the richness of the essay (unique words ratio).
    - Richness score is the ratio of unique words to total words.
    - Multiply the richness score by 50 to get the richness marks.
    """
    words = content.split()
    unique_words = set(words)
    richness_score = len(unique_words) / len(words) if words else 0
    return richness_score * 50
