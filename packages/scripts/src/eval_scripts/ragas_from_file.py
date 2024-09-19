import logging
from dotenv import load_dotenv
import os
import sys
import nest_asyncio
from datasets import Dataset
import pandas as pd
from langchain_community.document_loaders import DirectoryLoader
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.service_context import ServiceContext
from typing import Tuple, List, Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TEST_SIZE = 10
STEP_SIZE = 10

nest_asyncio.apply()

def main():
    load_dotenv()
    DB_SERVER = "localhost:2301"
    API_ENDPOINT_QA = "/api/datasets/add"
    API_ENDPOINT_COMP = "/api/completions/add"
    PATH_OUT = "output/completions/file"
    PATH_DATA = os.path.abspath(sys.argv[1])
    
    logging.info("Loading documents from path: %s", PATH_DATA)
    documents = load_documents(PATH_DATA)
    # id, metadata[page_label, file_name, file_path], text
    
    logging.info("Generating test set from documents (Question, Answer/Ground-Truth")
    dataset = generate_testset(documents, TEST_SIZE)
    # question, contexts, ground_truth, evolution_type, metadata

    # POST dataset to server if available
    if check_server_availability(DB_SERVER):
        logging.info("Data server is available. Saving Q-A dataset...")
        if post_dataset_to_server(dataset.to_dict(), DB_SERVER, API_ENDPOINT_QA):
            logging.info("Dataset successfully posted to server.")
            exit()
        else:
            logging.error("Failed to post Q-A dataset to server.")
    else:
        logging.info("Data server is not available")


def load_documents(path_data: str) -> List[Dict[str, Any]]:
    if os.path.isdir(path_data):
        reader = SimpleDirectoryReader(input_dir=path_data, num_files_limit=1, required_exts=[".pdf"])
    else:
        reader = SimpleDirectoryReader(input_files=[path_data], num_files_limit=1, required_exts=[".pdf"])
    return reader.load_data()

def initialize_generator() -> Tuple[TestsetGenerator, OpenAIEmbeddings]:
    generator_llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
    critic_llm = ChatOpenAI(model="gpt-4")
    embeddings = OpenAIEmbeddings()
    generator = TestsetGenerator.from_langchain(
        generator_llm,
        critic_llm,
        embeddings
    )
    return generator, embeddings

def generate_testset(documents: List[Dict[str, Any]], test_size: int) -> TestsetGenerator:
    logging.info("Initializing test set generator")
    generator, embeddings = initialize_generator()
    # Generate test set in batches
    ds_list = []
    for i in range(0, len(documents), STEP_SIZE):
        docs = documents[i:i+STEP_SIZE]
        df = generator.generate_with_llamaindex_docs(docs, test_size=test_size, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25}).to_pandas()
        ds_list.append(df)

    return Dataset.from_pandas(pd.concat(ds_list))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: python ragas_from_file.py <path_to_data>")
        exit
    main()
