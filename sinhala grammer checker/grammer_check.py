import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer
import nltk
from nltk.tokenize import word_tokenize
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("fill-mask", model="Ransaka/sinhala-bert-medium-v2")

# Load SinhalaBERT
# model_name = "HuggingFace/SinhalaBERT"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForMaskedLM.from_pretrained(model_name)
# Load model directly
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("Ransaka/sinhala-bert-medium-v2")
model = AutoModelForMaskedLM.from_pretrained("Ransaka/sinhala-bert-medium-v2")

# Function to validate Sinhala text
def validate_sinhala_text(text):
    sinhala_chars = "අඅආඇඈඉඊඋඌඍඎඏඐඑඒඓඔඕඖකඛගඝචඡජඣටඨඩඪණඬතථදධනඳපඵබභමඹයරලවශෂසහළෆ"
    return any(char in sinhala_chars for char in text)

# Grammar checking function
def check_sinhala_grammar(sentence):
    tokens = word_tokenize(sentence)
    total_words = len(tokens)
    correct_predictions = 0

    for i in range(total_words):
        temp_tokens = tokens[:]
        temp_tokens[i] = "[MASK]"
        masked_sentence = " ".join(temp_tokens)

        inputs = tokenizer(masked_sentence, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        masked_index = inputs["input_ids"][0].tolist().index(tokenizer.mask_token_id)
        predicted_token_id = torch.argmax(outputs.logits[0, masked_index]).item()
        predicted_word = tokenizer.decode([predicted_token_id])

        if predicted_word == tokens[i]:
            correct_predictions += 1

    score = (correct_predictions / total_words) * 100
    return f"Grammar Score: {score:.2f}% ({correct_predictions}/{total_words} words correct)"

# Take user input and validate
user_input = input("Enter a Sinhala sentence: ")
if validate_sinhala_text(user_input):
    print(check_sinhala_grammar(user_input))
else:
    print("Error: Please enter a valid Sinhala sentence.")


