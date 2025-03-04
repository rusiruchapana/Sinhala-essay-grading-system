from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import re

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

def preprocess_sinhala_text(text):
    text = re.sub(r'[^\u0D80-\u0DFF\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def check_relevance(essay, topic):
    model = SentenceTransformer(MODEL_NAME)
    clean_essay = preprocess_sinhala_text(essay)
    clean_topic = preprocess_sinhala_text(topic)

    max_chunk_length = 500
    essay_chunks = [clean_essay[i:i+max_chunk_length] for i in range(0, len(clean_essay), max_chunk_length)]

    essay_embeddings = [model.encode(chunk) for chunk in essay_chunks]
    topic_embedding = model.encode(clean_topic)

    total_similarity = sum(cosine_similarity([emb], [topic_embedding])[0][0] for emb in essay_embeddings)
    avg_similarity = total_similarity / len(essay_embeddings)

    return avg_similarity * 100  # Convert to percentage

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("0")  # Return 0 if invalid input
        sys.exit(1)

    essay = sys.argv[1]
    topic = sys.argv[2]

    relevance_score = check_relevance(essay, topic)
    print(f"{relevance_score:.2f}")  # Print only the score
