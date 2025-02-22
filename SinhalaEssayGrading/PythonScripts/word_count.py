import sys
import json

def calculate_word_count_score(essay_text, expected_word_count):
    actual_count = len(essay_text.split())
    score = min(10, (actual_count / expected_word_count) * 10) if expected_word_count > 0 else 0
    return round(score, 2)

if __name__ == "__main__":
    data = json.loads(sys.argv[1])
    essay_text = data["EssayText"]
    expected_word_count = data["ExpectedWordCount"]
    result = {"Word Count Score": calculate_word_count_score(essay_text, expected_word_count)}
    print(json.dumps(result))
