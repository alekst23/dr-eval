import json
from typing import List

class EmbeddingType:
    id: str
    embedding: List[float]

    def __init__(self, embedding: List[float], id: str = None):
        self.id = id
        self.embedding = embedding

    def to_dict(self):
        return {
            'id': self.id,
            'embedding': self.embedding
        }

    @staticmethod
    def from_dict(data: dict):
        return EmbeddingType(
            id=data.get('id'),
            embedding=data.get('embedding')
        )

    @staticmethod
    def from_tuple(data: tuple):
        if not data:
            return None
        return EmbeddingType(
            id=data[0],
            embedding=json.loads(data[1])
        )

class EmbeddingModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS embeddings (
                            id TEXT PRIMARY KEY,
                            embedding TEXT NOT NULL
                        )''')

    def add_embedding(self, embedding: EmbeddingType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO embeddings (id, embedding)
                                        VALUES (?, ?)''', (embedding.id, json.dumps(embedding.embedding),))
            return cursor.lastrowid

    def get_embedding_by_id(self, embedding_id: int):
        cursor = self.db.execute('''SELECT * FROM embeddings WHERE id = ?''', (embedding_id,))
        row = cursor.fetchone()
        if row:
            return EmbeddingType.from_tuple(row)
        return None

    def update_embedding(self, embedding: EmbeddingType):
        with self.db:
            cursor = self.db.execute('''UPDATE embeddings SET embedding = ? WHERE id = ?''', 
                                     (json.dumps(embedding.embedding), embedding.id))
            return cursor.rowcount > 0

    def delete_embedding(self, embedding_id: int):
        with self.db:
            cursor = self.db.execute('''DELETE FROM embeddings WHERE id = ?''', (embedding_id,))
            return cursor.rowcount > 0

    def get_all_embeddings(self):
        cursor = self.db.execute('''SELECT * FROM embeddings''')
        embeddings = [EmbeddingType.from_tuple(row) for row in cursor.fetchall()]
        return embeddings