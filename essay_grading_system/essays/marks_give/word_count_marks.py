# essays/marks_give/word_count_marks.py

def calculate_word_count_marks(word_count, required_word_count):
    """
    Calculate marks based on whether the essay meets the required word count.
    - If the word count is met or exceeded, award 50 marks.
    - Otherwise, award 0 marks.
    """
    return 50 if word_count >= required_word_count else 0