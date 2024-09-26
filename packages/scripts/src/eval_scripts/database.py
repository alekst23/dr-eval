from sqlite3 import Connection
from llama_index.core.schema import TextNode

from eval_data.models.embedding import EmbeddingModel, EmbeddingType


from logging import getLogger
logger = getLogger(__name__)

def upsert_text_node(db: Connection, text: str, id: str, embedding) -> TextNode:
    logger.info(f"upsert_text_node: {id}")
    embed_model = EmbeddingModel(db)
    if embed := embed_model.get_embedding_by_id(id):
        embedding_value = embed.embedding
    else:
        logger.info(f"new embedding for {id}")
        embedding_value = embedding
        embed_model.add_embedding(EmbeddingType(id=id, embedding=embedding_value))
    
    return TextNode(
        id_=id,
        text=text,
        embedding=embedding_value
    )