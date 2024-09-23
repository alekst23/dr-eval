import os
from typing import List

from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.schema import Document, TextNode
from datasets import load_dataset

from eval_data.models.document import DocumentModel, DocumentType
from .embeddings import get_embeddings

from logging import getLogger
logger = getLogger(__name__)


def load_documents(doclist: List[DocumentType]) -> List[TextNode]:
    documents = []
    for doc in doclist:
        if doc.source == "huggingface":
            documents.extend(load_huggingface_documents([doc]))
        elif doc.source == "file":
            documents.extend(load_documents_from_path(doc.location))
        else:
            raise ValueError(f"Unknown source: {doc.source}")
    return documents

def load_huggingface_documents(doclist: List[DocumentType]) -> List[TextNode]:
    documents = []
    for doc in doclist:
        logger.info(f"load_huggingface_document: {doc.location}")
        print(f"load_huggingface_document: {doc.location}")
        path, name = doc.location.split(";")
        doc_loader = load_dataset(path=path, name=name, streaming=True)
        print(f"collecting documents from {doc.location}")
        for i, doc in enumerate(doc_loader["passages"]):
            print(f"loading document {i}")
            if doc["passage"]:
                try:
                    documents.append(
                        TextNode(
                            text=doc["passage"],
                            embedding=get_embeddings(doc["passage"]),
                            id_=str(doc["id"])
                        ) 
                    )
                except Exception as e:
                    print(f"Error loading document: {e}")

    return documents


def load_documents_from_path(path_data: str) -> List[Document]:
    if os.path.isdir(path_data):
        reader = SimpleDirectoryReader(input_dir=path_data, num_files_limit=1, required_exts=[".pdf"])
    else:
        reader = SimpleDirectoryReader(input_files=[path_data], num_files_limit=1, required_exts=[".pdf"])
    return reader.load_data()

