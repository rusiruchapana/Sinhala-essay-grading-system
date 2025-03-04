import sys
import json
import subprocess
from grading_utils import grade_essay
from vocabulary_richness import calculate_vocabulary_richness

# Define the path to the relevance checking script
RELEVANCE_SCRIPT_PATH = "C:\\Users\\umega\\Desktop\\Research\\Sinhala-essay-grading-system\\SinhalaEssayGrading\\PythonScripts\\relevance_checker_enhanced.py"

def check_relevance(essay_text, topic):
    """Runs the relevance checking script and returns the score."""
    try:
        result = subprocess.run(
            ["python", RELEVANCE_SCRIPT_PATH, essay_text, topic],
            capture_output=True,
            text=True
        )
        relevance_score = float(result.stdout.strip())  # Get the score from output
        return relevance_score
    except Exception as e:
        print(f"Error running relevance checker: {e}")
        return 0.0  # Default to 0 if error occurs

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
    relevance_score = check_relevance(essay_text, topic)

    # Combine scores with weight adjustments
    total_score = (result["word_count_score"] * 0.4) + (richness_score * 0.3) + (relevance_score * 0.3)

    # Add scores to result
    result["richness_score"] = richness_score
    result["relevance_score"] = relevance_score
    result["total_score"] = total_score

    print(json.dumps(result))

if __name__ == "__main__":
    main()
