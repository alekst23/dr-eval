from typing import List
#from llama_index.llms import OpenAI
from datasets.arrow_dataset import Dataset

from eval_scripts.utils import chunk_documents
from packages.scripts.src.eval_scripts.generator import AbstractGenerator, QueryResponse, ResponseContext

from packages.ragtag.src.ragtag.backend.ragtag import RagTag
from packages.ragtag.src.ragtag.db.db_connection import DBConnection

from openai import OpenAI

from logging import getLogger
logger = getLogger(__name__)


class RagTagInstance(AbstractGenerator):

    def __init__(self, nodes: List[Dataset], db_connection: DBConnection=None):
        if db_connection is None:
            db_connection = DBConnection(":memory:")
             
        self.ragtag = RagTag(db_connection)
        self.ragtag.add_documents_bulk([node.text for node in nodes])
        self.ragtag.init_vector_store()
        self.client = OpenAI()


    def query(self, query: str) -> QueryResponse:
        docs = self.ragtag.search_documents(query)

        context = "### document:".join([doc["text"] for doc in docs])
        context = "# Document list:\n" + context
        
        messages = [
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": query
            }
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response_text = response.choices[0].message.content
        
        return QueryResponse(
            query=query,
            response=response_text,
            context=[ResponseContext(score=doc["score"], text=doc["text"]) for doc in docs]
        )


def build_query_engine(nodes: List[Dataset]) -> RagTagInstance:
    db_connection = DBConnection("ragtag.db")
    return RagTagInstance(nodes=nodes, db_connection=db_connection)