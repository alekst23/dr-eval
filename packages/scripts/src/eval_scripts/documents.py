import os
from typing import List
from sqlite3 import Connection
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.schema import Document, TextNode

from eval_data.models.document import DocumentType
from eval_scripts.hface import load_huggingface_document

from logging import getLogger
logger = getLogger(__name__)


def load_documents(db: Connection, doclist: List[DocumentType]) -> List[TextNode]:
    documents = []
    for doc in doclist:
        if doc.source == "huggingface":
            documents.extend(load_huggingface_document(db, doc))
        elif doc.source == "file":
            documents.extend(load_documents_from_path(doc.location))
        else:
            raise ValueError(f"Unknown source: {doc.source}")
    return documents


def load_documents_from_path(path_data: str) -> List[Document]:
    if os.path.isdir(path_data):
        reader = SimpleDirectoryReader(input_dir=path_data, num_files_limit=1, required_exts=[".pdf"])
    else:
        reader = SimpleDirectoryReader(input_files=[path_data], num_files_limit=1, required_exts=[".pdf"])
    return reader.load_data()

