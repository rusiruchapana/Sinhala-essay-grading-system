import sys
import json
from grading_utils import grade_essay
from vocabulary_richness import calculate_vocabulary_richness

def main():
    if len(sys.argv) != 2:
        print("Usage: python grade_essay.py <input_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    essay_text = input_data.get("EssayText", "")
    expected_word_count = input_data.get("ExpectedWordCount", 0)
    topic = input_data.get("Topic", "")

    # Get grading scores
    result = grade_essay(essay_text, expected_word_count, topic)
    richness_score = calculate_vocabulary_richness(essay_text)

    # Combine scores with weight adjustments
    total_score = (result["word_count_score"] * 0.4) + (richness_score * 0.6)

    # Add scores to result
    result["richness_score"] = richness_score
    result["total_score"] = total_score

    print(json.dumps(result))

if __name__ == "__main__":
    main()
