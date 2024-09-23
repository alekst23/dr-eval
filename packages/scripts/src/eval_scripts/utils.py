import requests
from typing import Dict, Any, List
from llama_index.core.schema import TextNode
import math
import tiktoken

from logging import getLogger
logger = getLogger(__name__)

DB_SERVER = "http://127.0.0.1:2301/"
API_ENDPOINT_DATASET = "api/datasets/add_dataset"
API_ENDPOINT_DOCS = "api/datasets/add_document"
API_ENDPOINT_QA = "api/datasets/add_qaset"

HEADERS = {'Content-Type': 'application/json'}

def post_to_server(data: Dict[str, Any], server_url: str, api_endpoint: str) -> dict:
    try:
        response = requests.post(server_url + api_endpoint, json=data, headers=HEADERS)
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        else:
            logger.error(f"Error: {response.status_code}")
            return {"error": response.status_code}
    except Exception as e:
        logger.exception(str(e))
        return {"error": "Server not available"}

def post_dataset(data: dict):
    return post_to_server(data, DB_SERVER, API_ENDPOINT_DATASET)
    
def post_documents(data: dict):
    return post_to_server(data, DB_SERVER, API_ENDPOINT_DOCS)

def post_qasets(data: dict):
    return post_to_server(data, DB_SERVER, API_ENDPOINT_QA)

def chunk_documents(doc_list: List[TextNode], max_tokens=8192) -> list[TextNode]:
    OVERLAP = 10
    documents = []
    for doc in doc_list:
        if (tokens:=count_tokens(doc.text)) and tokens > max_tokens:
            print(f"Document {doc.id_} has {tokens} tokens")
            # chunk document into smaller pieces
            chunks = []
            max_chunks = math.ceil(tokens / max_tokens)
            words = doc.text.split(" ")
            for i in range(0, max_chunks):
                start = i * len(words) // max_chunks
                end = (i + 1) * len(words) // max_chunks + OVERLAP
                
                chunks.append(" ".join(words[start:end]))

            print(f"Chunked into {len(chunks)} pieces")
            for i, chunk in enumerate(chunks):
                documents.append(TextNode(text=chunk, id_=f"{doc.id_}-{i}"))
        else:
            documents.append(doc)

    return documents


def count_tokens(text):
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")  # or whichever model you're using
    return len(tokenizer.encode(text))
