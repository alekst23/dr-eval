from typing import Optional, List

class QASetType:
    id: Optional[int]
    datasource_id: int
    document_id: int
    name: str
    location: str

    def __init__(self,datasource_id: int, document_id: int, name: str, location: str, id: int = None):
        self.id = id
        self.datasource_id = datasource_id
        self.document_id = document_id
        self.name = name
        self.location = location

    def to_dict(self):
        return {
            'id': self.id,
            'datasource_id': self.datasource_id,
            'document_id': self.document_id,
            'name': self.name,
            'location': self.location
        }

    @staticmethod
    def from_dict(data: dict):
        return QASetType(
            id=data.get('id'),
            datasource_id=data.get('datasource_id'),
            document_id=data.get('document_id'),
            name=data.get('name'),
            location=data.get('location')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        if not data:
            return None
        return QASetType(
            id=data[0],
            datasource_id=data[1],
            document_id=data[2],
            name=data[3],
            location=data[4]
        )

class QASetModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS qasets (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            datasource_id INTEGER NOT NULL,
                            document_id INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            location TEXT NOT NULL,
                            FOREIGN KEY(datasource_id) REFERENCES datasources(id),
                            FOREIGN KEY(document_id) REFERENCES documents(id)
                        )''')

    def add_qaset(self, qaset: QASetType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO qasets (datasource_id, document_id, name, location)
                                        VALUES (?, ?, ?, ?)''', (qaset.datasource_id, qaset.document_id, qaset.name, qaset.location))
            return cursor.lastrowid

    def get_qaset_by_id(self, qaset_id: int) -> Optional[QASetType]:
        cursor = self.db.execute('''SELECT * FROM qasets WHERE id = ?''', (qaset_id,))
        row = cursor.fetchone()
        if row:
            return QASetType.from_tuple(row)
        return None
    
    def get_qaset_by_name(self, name):
        cursor = self.db.execute('''SELECT * FROM qasets WHERE name = ?''', (name,))
        return QASetType.from_tuple(cursor.fetchone())

    def get_qasets_by_document_id(self, document_id):
        cursor = self.db.execute('''SELECT * FROM qasets WHERE document_id = ?''', (document_id,))
        qasets = [QASetType.from_tuple(row) for row in cursor.fetchall()]
        return qasets

    def get_qasets_by_datasource_id(self, datasource_id):
        cursor = self.db.execute('''SELECT * FROM qasets WHERE datasource_id = ?''', (datasource_id,))
        qasets = [QASetType.from_tuple(row) for row in cursor.fetchall()]
        return qasets

    def get_all_qasets(self) -> List[QASetType]:
        cursor = self.db.execute('''SELECT * FROM qasets''')
        rows = cursor.fetchall()
        return [QASetType.from_tuple(row) for row in rows]

    def update_qaset(self, qaset: QASetType) -> bool:
        with self.db:
            cursor = self.db.execute('''UPDATE qasets SET datasource_id = ?, document_id = ?, name = ?, location = ?
                                        WHERE id = ?''', (qaset.datasource_id, qaset.document_id, qaset.name, qaset.location, qaset.id))
            return cursor.rowcount > 0

    def delete_qaset(self, qaset_id: int) -> bool:
        with self.db:
            cursor = self.db.execute('''DELETE FROM qasets WHERE id = ?''', (qaset_id,))
            return cursor.rowcount > 0

