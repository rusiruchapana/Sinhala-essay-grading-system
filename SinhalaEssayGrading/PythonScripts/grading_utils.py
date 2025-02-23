def grade_essay(essay_text, expected_word_count, topic):
    word_count = len(essay_text.split())
    word_count_score = min(word_count / expected_word_count, 1.0) * 100  # Score out of 100

    return {
        "word_count_score": word_count_score
    }
