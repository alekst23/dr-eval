from dotenv import load_dotenv
load_dotenv()

import os
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.service_context import ServiceContext
from llama_index.core.node_parser import SimpleNodeParser
from datasets import Dataset, load_dataset
from llama_index.core.schema import TextNode

PATH_OUT = "tests/data/output/completions/sample"

def main():
    dataset = load_dataset("rag-datasets/rag-mini-bioasq", "question-answer-passages")['test']
    doc_loader = load_dataset("rag-datasets/rag-mini-bioasq", "text-corpus")

    documents = [ TextNode(text=doc["passage"], id_=doc["id"]) for doc in doc_loader["passages"] ]

    test_questions = dataset["question"]
    if "ground_truth" in dataset.column_names:
        test_answers = dataset["ground_truth"]
    else:
        test_answers = dataset["answer"]

    query_engine1 = build_query_engine(documents)
    result_ds = generate_responses(query_engine1, test_questions, test_answers)

    result_ds.save_to_disk(PATH_OUT)


def build_query_engine(nodes, persist_dir="./storage"):
    # Check if we have a persisted index
    if os.path.exists(persist_dir):
        # Load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        vector_index = load_index_from_storage(storage_context)
    else:
        # Create a new index
        vector_store = SimpleVectorStore()
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


# Function to evaluate as Llama index does not support async evaluation for HFInference API
def generate_responses(query_engine, test_questions, test_answers):
    responses = [query_engine.query(q) for q in test_questions]

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
    ds = Dataset.from_dict(dataset_dict)
    return ds
