import requests
import os
from typing import Dict, Any, List
import os
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.schema import TextNode
from datasets.arrow_dataset import Dataset
import math
import tiktoken
import chromadb

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

def build_query_engine(nodes: List[Dataset], persist_dir="./storage"):
    '''
    Build a query engine from a list of documents
    
    nodes : List[Dataset]
        List of {id, passage} dictionaries
    persist_dir : str
        Directory to save the index
    '''
    logger.info("Building query engine")

    # Split documents that are longer than 8192 tokens
    nodes = chunk_documents(nodes)

    # Create a new index
    # vector_store = SimpleVectorStore()
    # create client and a new collection
    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.create_collection("quickstart")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # If nodes are already TextNode objects, we can use them directly
    # If not, we need to parse them into TextNodes
    if not isinstance(nodes[0], TextNode):
        parser = SimpleNodeParser()
        nodes = parser.get_nodes_from_documents(nodes)
    
    vector_index = VectorStoreIndex(
        nodes,
        storage_context=storage_context
    )

    # Persist the index
    vector_index.storage_context.persist(persist_dir=persist_dir)

    query_engine = vector_index.as_query_engine(similarity_top_k=3)
    return query_engine


def load_query_engine(persist_dir="./storage"):
    logger.info("Loading query engine")
    if os.path.exists(persist_dir):
        chroma_client = chromadb.EphemeralClient()
        chroma_collection = chroma_client.get_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=persist_dir)
        vector_index = load_index_from_storage(storage_context)
        return vector_index.as_query_engine(similarity_top_k=3)
    else:
        return None


def count_tokens(text):
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")  # or whichever model you're using
    return len(tokenizer.encode(text))
