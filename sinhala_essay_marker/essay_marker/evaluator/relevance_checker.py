from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Load model once (globally)
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
model = SentenceTransformer(MODEL_NAME)

def preprocess_sinhala_text(text):
    """Clean Sinhala text by removing non-Sinhala characters and extra spaces"""
    text = re.sub(r'[^\u0D80-\u0DFF\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def encode_chunks(chunks):
    """Encode text chunks in parallel"""
    with ThreadPoolExecutor() as executor:
        embeddings = list(executor.map(model.encode, chunks))
    return embeddings

def calculate_relevance_marks(essay, topic):
    """
    Calculate marks based on how relevant the essay is to the given topic
    Returns marks out of 100 as native Python float
    """
    # Preprocess text
    clean_essay = preprocess_sinhala_text(essay)
    clean_topic = preprocess_sinhala_text(topic)
    
    if not clean_essay or not clean_topic:
        return 0.0  # Return native float
    
    try:
        # Handle long essays by splitting into chunks
        max_chunk_length = 1000
        essay_chunks = [clean_essay[i:i+max_chunk_length] 
                       for i in range(0, len(clean_essay), max_chunk_length)]
        
        # Generate embeddings
        essay_embeddings = encode_chunks(essay_chunks)
        topic_embedding = model.encode(clean_topic)
        
        # Calculate similarity
        combined_essay_embedding = np.mean(essay_embeddings, axis=0)
        similarity = cosine_similarity(
            [combined_essay_embedding], 
            [topic_embedding]
        )[0][0]
        
        # Convert to native Python float before returning
        return float(max(0.0, min(100.0, similarity * 100)))
    
    except Exception as e:
        print(f"Error in relevance calculation: {e}")
        return 0.0  # Return native float