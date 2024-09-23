from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # Smaller and efficient for sentence embeddings

def get_embeddings(text):
    return model.encode(text).tolist()