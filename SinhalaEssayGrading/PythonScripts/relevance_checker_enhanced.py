from sentence_transformers import SentenceTransformer
import numpy as np
import re
import sys

# Load the model once at startup
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
MODEL = SentenceTransformer(MODEL_NAME)

def preprocess_sinhala_text(text):
    """Remove non-Sinhala characters and extra whitespace."""
    text = re.sub(r'[^\u0D80-\u0DFF\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def check_relevance(essay, topic):
    """Compute the relevance score between the essay and topic."""
    clean_essay = preprocess_sinhala_text(essay)
    clean_topic = preprocess_sinhala_text(topic)

    # Split long essays into chunks
    max_chunk_length = 500
    essay_chunks = [clean_essay[i:i+max_chunk_length] for i in range(0, len(clean_essay), max_chunk_length)]

    # Encode all chunks at once (Batch Processing)
    essay_embeddings = MODEL.encode(essay_chunks, convert_to_numpy=True)
    topic_embedding = MODEL.encode(clean_topic, convert_to_numpy=True)

    # Use NumPy for faster cosine similarity
    similarity_scores = np.dot(essay_embeddings, topic_embedding) / (np.linalg.norm(essay_embeddings, axis=1) * np.linalg.norm(topic_embedding))

    # Compute final relevance score
    avg_similarity = np.mean(similarity_scores) * 100
    return avg_similarity

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("0")  # Return 0 if input is invalid
        sys.exit(1)

    essay = sys.argv[1]
    topic = sys.argv[2]

    relevance_score = check_relevance(essay, topic)
    print(f"{relevance_score:.2f}")  # Print only the score
