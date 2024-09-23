from typing import Literal

class DocumentType:
    id: int
    datasource_id: int
    name: str
    location: str
    source: Literal["huggingface", "file"]

    def __init__(self, datasource_id: int, name: str, location: str, id: int = None, source: str = "huggingface"):
        self.id = id
        self.datasource_id = datasource_id
        self.name = name
        self.location = location
        self.source = source

    def to_dict(self):
        return {
            'id': self.id,
            'datasource_id': self.datasource_id,
            'name': self.name,
            'location': self.location,
            'source': self.source
        }

    @staticmethod
    def from_dict(data: dict):
        return DocumentType(
            id=data.get('id'),
            datasource_id=data.get('datasource_id'),
            name=data.get('name'),
            location=data.get('location'),
            source=data.get('source')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        if not data:
            return
        return DocumentType(
            id=data[0],
            datasource_id=data[1],
            name=data[2],
            location=data[3],
            source=data[4]
        )

class DocumentModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS documents (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            datasource_id INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            location TEXT NOT NULL,
                            source TEXT NOT NULL,
                            FOREIGN KEY(datasource_id) REFERENCES datasources(id)
                        )''')

    def add_document(self, document: DocumentType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO documents (datasource_id, name, location, source)
                                        VALUES (?, ?, ?, ?)''', (document.datasource_id, document.name, document.location, document.source))
            return cursor.lastrowid

    def add_or_get_document(self, document: DocumentType):
        existing_document = self.get_document_by_name(document.name)
        if existing_document:
            return existing_document
        document.id = self.add_document(document)
        return document

    def get_documents_by_datasource(self, datasource_id):
        cursor = self.db.execute('''SELECT * FROM documents WHERE datasource_id = ?''', (datasource_id,))
        documents = [DocumentType.from_tuple(row) for row in cursor.fetchall()]
        return documents

    def delete_document(self, document_id):
        with self.db:
            cursor = self.db.execute('''DELETE FROM documents WHERE id = ?''', (document_id,))
            return cursor.rowcount > 0

    def update_document(self, doc: DocumentType):
        with self.db:
            cursor = self.db.execute('''UPDATE documents SET name = ?, location = ?, source = ? WHERE id = ?''', (doc.name, doc.location, doc.source, doc.id))
            return cursor.rowcount > 0

    def get_document_by_id(self, document_id):
        cursor = self.db.execute('''SELECT * FROM documents WHERE id = ?''', (document_id,))
        row = cursor.fetchone()
        if row:
            return DocumentType.from_tuple(row)
        return None

    def get_document_by_name(self, name):
        cursor = self.db.execute('''SELECT * FROM documents WHERE name = ?''', (name,))
        document = DocumentType.from_tuple(cursor.fetchone())
        return document
