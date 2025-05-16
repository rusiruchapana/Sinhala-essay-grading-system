def calculate_word_count_marks(essay, required_word_count):
    """
    Calculate marks based on word count with intelligent penalties.
    Returns marks out of 100, with:
    - Full marks for being within a grace range (±10%).
    - Progressive penalties for deviations beyond the grace range.
    - Zero marks only for extreme cases (<40% or >250%).

    Args:
        essay (str): The essay text.
        required_word_count (int): Target word count.

    Returns:
        float: Marks between 0 and 100.
    """
    word_count = len(essay.split())
    percentage = word_count / required_word_count

    # Grace range (±10%): No penalty (full marks)
    if 0.9 <= percentage <= 1.1:
        return 100.0

    # Under word count penalties (below 90%)
    elif percentage < 0.9:
        if percentage < 0.4:  # Extremely short (0 marks)
            return 0.0
        elif percentage < 0.7:  # Moderately short (linear penalty: 50-80%)
            return max(50.0, round(80 * percentage, 2))
        else:  # Slightly short (80-90%)
            return max(80.0, round(90 * percentage, 2))

    # Over word count penalties (above 110%)
    else:
        if percentage > 2.5:  # Extremely long (0 marks)
            return 0.0
        elif percentage > 1.5:  # Very long (steep penalty: 30-70%)
            penalty = (percentage - 1.1) * 100  # 110-250% → 90% → 0%
            return max(30.0, round(100 - penalty, 2))
        else:  # Slightly long (70-90%)
            penalty = (percentage - 1.1) * 50  # 110-150% → 5% per 10% over
            return max(70.0, round(100 - penalty, 2))