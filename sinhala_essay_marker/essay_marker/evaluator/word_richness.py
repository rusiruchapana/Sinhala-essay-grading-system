def calculate_word_richness_marks(essay):
    """
    Calculate marks based on word richness (variety of words used).
    Returns marks out of 100 (100% of total marks).
    This is a simplified version - you might want to enhance it.
    """
    words = essay.split()
    total_words = len(words)
    
    if total_words == 0:
        return 0
    
    unique_words = set(words)
    unique_word_count = len(unique_words)
    
    # Calculate richness ratio (unique words vs total words)
    richness_ratio = unique_word_count / total_words
    
    # Scale to 100 marks
    return round(richness_ratio * 100, 2)