from datasets import load_dataset
from typing import List
from sqlite3 import Connection
from llama_index.core.schema import TextNode
from datasets import load_dataset

from eval_data.models.qaset import QASetType
from eval_data.models.document import DocumentType
from .database import upsert_text_node

from logging import getLogger
logger = getLogger(__name__)

def load_qa_dataset(qaset: QASetType):
    location = qaset.location.split(";")
    path = location[0]
    name = location[1] if len(location) > 1 else None

    logger.info(f"Loading HuggingFace dataset from {location}")

    dataset_dict = load_dataset(path, name)
    dataset = dataset_dict[list(dataset_dict.keys())[0]]

    test_questions = dataset[qaset.col_question]
    test_answers = dataset[qaset.col_answer]

    return test_questions, test_answers

def load_huggingface_document(db: Connection, document: DocumentType) -> List[TextNode]:
    logger.info(f"load_huggingface_document: {document.location}")
    location = document.location.split(";")
    path = location[0]
    name = location[1] if len(location) > 1 else None
    doc_dict = load_dataset(path=path, name=name, streaming=True)

    logger.info(f"collecting text nodes from {document.location}")
    nodes = []
    for i, doc in enumerate(doc_dict[list(doc_dict.keys())[0]]):
        logger.info(f"loading document {i}")
        if doc[document.col_text]:
            try:
                id = f"{document.id}_{doc[document.col_id] if document.col_id and document.col_id in doc else i}"
                if isinstance(doc[document.col_text], list):
                    for j, text in enumerate(doc[document.col_text]):
                        nodes.append(
                            upsert_text_node(db, text, f"{id}_{j}")
                        )
                else:
                    nodes.append(
                        upsert_text_node(db, doc[document.col_text], id)
                    )
            except Exception as e:
                logger.warning(f"Error loading document: {e}")

    return nodes