import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python grade_essay.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    # Read JSON data from the file
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(json.dumps({"Word Count Score": 10}))  # Example output for debugging
