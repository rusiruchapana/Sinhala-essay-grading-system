import re

def calculate_vocabulary_richness(essay_text):
    words = re.findall(r'\b\w+\b', essay_text)  # Extract words
    unique_words = set(words)  # Get unique words

    if len(words) == 0:
        return 0  # Avoid division by zero

    richness_score = (len(unique_words) / len(words)) * 100  # Normalize to 100
    return min(richness_score, 100)  # Ensure max is 100
