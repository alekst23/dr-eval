import os
from typing import Dict, Any, List
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.indices import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.schema import TextNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama_index.llms import OpenAI
from datasets.arrow_dataset import Dataset
import chromadb

from eval_scripts.utils import chunk_documents
from packages.scripts.src.eval_scripts.generator import AbstractGenerator


from logging import getLogger
logger = getLogger(__name__)


COLLECTION_NAME = "quickstart"
PERSIST_DIR = "./storage"

class LlamaIndex(AbstractGenerator):

    def __init__(self, nodes: List[Dataset]):
        logger.info("Building llama_index query engine")

        # Split documents that are longer than 8192 tokens
        nodes = chunk_documents(nodes)

        # Create a new index
        # vector_store = SimpleVectorStore()
        # create client and a new collection
        chroma_client = chromadb.EphemeralClient()
        try:
            chroma_collection = chroma_client.get_collection(COLLECTION_NAME)
            logger.info(f"Collection {COLLECTION_NAME} already exists")
        except Exception as e:
            chroma_collection = chroma_client.create_collection(COLLECTION_NAME)
            logger.info(f"Created collection {COLLECTION_NAME}")

        # Save nodes to collection
        logger.info("Saving nodes to collection")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        # Batch add
        BATCH_SIZE = 500
        for i in range(0, len(nodes), BATCH_SIZE):
            vector_store.add(nodes[i:i+BATCH_SIZE])

        # Create embedding model
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

        #Create a new index
        logger.info("Building index")
        vector_index = VectorStoreIndex(
            nodes=nodes,
            vector_store=vector_store,
            node_parser=SimpleNodeParser(),
            embed_model=embed_model
        )

        # Persist the index
        logger.info("Persisting index")
        vector_index.storage_context.persist(persist_dir=PERSIST_DIR)

        #llm = OpenAI(model="gpt-4o-mini")
        self.query_engine = vector_index.as_query_engine(similarity_top_k=3)


    def load_query_engine(persist_dir=PERSIST_DIR):
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

    def query(self, query: str) -> List[Dict[str, Any]]:
        return self.query_engine.query(query)