from typing import Literal

class DocumentType:
    id: int
    datasource_id: int
    name: str
    location: str
    source: Literal["huggingface", "file"]
    col_text: str

    def __init__(self, datasource_id: int, name: str, location: str, id: int = None, source: str = "huggingface", col_text: str = ""):
        self.id = id
        self.datasource_id = datasource_id
        self.name = name
        self.location = location
        self.source = source
        self.col_text = col_text

    def to_dict(self):
        return {
            'id': self.id,
            'datasource_id': self.datasource_id,
            'name': self.name,
            'location': self.location,
            'source': self.source,
            'col_text': self.col_text
        }

    @staticmethod
    def from_dict(data: dict):
        return DocumentType(
            id=data.get('id'),
            datasource_id=data.get('datasource_id'),
            name=data.get('name'),
            location=data.get('location'),
            source=data.get('source'),
            col_text=data.get('col_text')
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
            source=data[4],
            col_text=data[5]
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
                            col_text TEXT,
                            FOREIGN KEY(datasource_id) REFERENCES datasources(id)
                        )''')

    def add_document(self, document: DocumentType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO documents (datasource_id, name, location, source, col_text)
                                        VALUES (?, ?, ?, ?, ?)''', (document.datasource_id, document.name, document.location, document.source, document.col_text))
            return cursor.lastrowid

    def add_or_get_document(self, document: DocumentType):
        existing_document = self.get_document_by_name(document.name)
        if existing_document:
            document.id = existing_document.id
            self.update_document(document)
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
            cursor = self.db.execute('''UPDATE documents SET datasource_id = ?, name = ?, location = ?, source = ?, col_text = ? WHERE id = ?''', (doc.datasource_id, doc.name, doc.location, doc.source, doc.col_text, doc.id))
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