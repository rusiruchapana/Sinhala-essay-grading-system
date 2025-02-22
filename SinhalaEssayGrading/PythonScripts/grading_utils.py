def grade_essay(essay_text, expected_word_count, topic):
    word_count = len(essay_text.split())
    word_count_score = min(word_count / expected_word_count, 1.0) * 100  # Score out of 100

    # Additional grading logic can be added here
    # For now, we only consider word count

    return {
        "word_count_score": word_count_score,
        "total_score": word_count_score  # Assuming total score is based on word count for now
    }