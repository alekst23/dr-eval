from datasets import load_dataset
from typing import List

from llama_index.core.schema import TextNode
from datasets import load_dataset

from eval_data.models.qaset import QASetType
from eval_data.models.document import DocumentType
from .embeddings import get_embeddings


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

def load_huggingface_documents(doclist: List[DocumentType]) -> List[TextNode]:
    documents = []
    for document in doclist:
        logger.info(f"load_huggingface_document: {document.location}")
        print(f"load_huggingface_document: {document.location}")
        location = document.location.split(";")
        path = location[0]
        name = location[1] if len(location) > 1 else None
        doc_dict = load_dataset(path=path, name=name, streaming=True)
        print(f"collecting documents from {document.location}")
        for i, doc in enumerate(doc_dict[list(doc_dict.keys())[0]]):
            print(f"loading document {i}")
            if doc[document.col_text]:
                try:
                    if isinstance(doc[document.col_text], list):
                        for i, text in enumerate(doc[document.col_text]):
                            documents.append(
                                TextNode(
                                    text=text,
                                    embedding=get_embeddings(text),
                                    #id_=str(i)+str(doc["id"])
                                ) 
                            )
                    else:
                        documents.append(
                            TextNode(
                                text=doc[document.col_text],
                                embedding=get_embeddings(doc[document.col_text]),
                                #id_=str(doc["id"])
                            ) 
                        )
                except Exception as e:
                    print(f"Error loading document: {e}")

    return documents