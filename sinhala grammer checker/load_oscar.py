from datasets import load_dataset

# Load the dataset
dataset = load_dataset("oscar",
    language="si",
    streaming=True, # optional
    split="train",
    trust_remote_code=True
    ) # optional

# Open a file to write the output
with open("output.txt", "w", encoding="utf-8") as file:
    for d in dataset:
        file.write(str(d) + "\n") # Write each document to the file
