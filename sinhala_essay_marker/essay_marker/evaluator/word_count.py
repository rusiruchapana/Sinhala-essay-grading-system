def calculate_word_count_marks(essay, required_word_count):
    """
    Calculate marks based on word count.
    Returns marks out of 100 (double the original marks).
    """
    word_count = len(essay.split())
    
    if word_count >= required_word_count:
        return 100
    else:
        # Deduct marks proportionally for shorter essays
        percentage = word_count / required_word_count
        return round(percentage * 100, 2)