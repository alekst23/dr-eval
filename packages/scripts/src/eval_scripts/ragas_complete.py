import logging
import os
import sys
from dotenv import load_dotenv
from datasets import Dataset
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.service_context import ServiceContext
from llama_index.core.readers import SimpleDirectoryReader
from typing import List, Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_query_engine(documents: List[Dict[str, Any]]) -> BaseQueryEngine:
    vector_index = VectorStoreIndex.from_documents(
        documents,
        service_context=ServiceContext.from_defaults(chunk_size=512),
    )
    return vector_index.as_query_engine(similarity_top_k=3)

def generate_responses(query_engine: VectorStoreIndex, test_questions: List[str], test_answers: List[str] | None) -> Dataset:
    
    logging.info(f"Generating completions for {len(test_questions)} questions")
    responses = [query_engine.query(q) for q in test_questions]

    logging.info("Composing Dataset from responses")
    answers = []
    contexts = []
    for r in responses:
        answers.append(r.response)
        contexts.append([c.node.get_content() for c in r.source_nodes])
    dataset_dict = {
        "question": test_questions,
        "answer": answers,
        "contexts": contexts,
    }
    if test_answers is not None:
        dataset_dict["ground_truth"] = test_answers
    return Dataset.from_dict(dataset_dict)


def load_documents(path_data: str) -> List[Dict[str, Any]]:
    if os.path.isdir(path_data):
        reader = SimpleDirectoryReader(input_dir=path_data, num_files_limit=1, required_exts=[".pdf"])
    else:
        reader = SimpleDirectoryReader(input_files=[path_data], num_files_limit=1, required_exts=[".pdf"])
    return reader.load_data()

