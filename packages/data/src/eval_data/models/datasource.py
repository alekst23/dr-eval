from typing import Optional

class DatasourceType:
    id: Optional[int]
    name: str
    description: Optional[str]
    created_at: Optional[int]

    def __init__(self, name: str, description: Optional[str] = None, id: Optional[int] = None, created_at: Optional[int] = None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data: dict):
        return DatasourceType(
            id=data.get('id'),
            name=data['name'],
            description=data.get('description'),
            created_at=data.get('created_at')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        return DatasourceType(
            id=data[0],
            name=data[1],
            description=data[2],
            created_at=data[3]
        )

class DatasourceModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS datasources (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')

    def add_datasource(self, data: DatasourceType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO datasources (name, description)
                                        VALUES (?, ?)''', (data.name, data.description))
            return cursor.lastrowid

    def add_or_get_datasource(self, data: DatasourceType):
        """Adds a new Datasource to the database if it does not exist, otherwise returns the existing record, matching by name."""
        existing_datasource = self.get_datasource_by_name( data.name )
        if existing_datasource:
            return existing_datasource
        else:
            data.id = self.add_datasource(data)
            return data

    def get_datasource_by_id(self, datasource_id):
        cursor = self.db.execute("SELECT * FROM datasources WHERE id = ?", (datasource_id,))
        row = cursor.fetchone()
        if row:
            return DatasourceType.from_tuple(row)
        return None

    def get_datasource_by_name(self, name):
        cursor = self.db.execute("SELECT * FROM datasources WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return DatasourceType.from_tuple(row)
        return None

    def get_all_datasources(self):
        cursor = self.db.execute("SELECT * FROM datasources")
        datasources = []
        for row in cursor.fetchall():
            datasources.append(DatasourceType.from_tuple(row))
        return datasources


    def update_datasource(self, datasource):
        with self.db:
            cursor = self.db.execute("UPDATE datasources SET name = ?, description = ? WHERE id = ?",
                    (datasource.name, datasource.description, datasource.id))
            return cursor.rowcount > 0


    def delete_datasource(self, datasource_id):
        with self.db:
            cursor = self.db.execute("DELETE FROM datasources WHERE id = ?", (datasource_id,))
            return cursor.rowcount > 0
