from transformers import AutoModel, AutoTokenizer
import torch

EMBEDDING_MODEL = "google-bert/bert-base-uncased"
model = AutoModel.from_pretrained(EMBEDDING_MODEL)
tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy().tolist()