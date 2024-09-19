from datetime import datetime

class TestRunType:
    def __init__(self, datasource_id: int, description: str, timestamp: str = None, id: int = None):
        self.id = id
        self.datasource_id = datasource_id
        self.description = description
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'id': self.id,
            'datasource_id': self.datasource_id,
            'description': self.description,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(data: dict):
        return TestRunType(
            id=data.get('id'),
            datasource_id=data.get('datasource_id'),
            description=data.get('description'),
            timestamp=data.get('timestamp')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        return TestRunType(
            id=data[0],
            datasource_id=data[1],
            description=data[2],
            timestamp=data[3]
        )

class TestRunModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS test_runs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            datasource_id INTEGER NOT NULL,
                            description TEXT NOT NULL,
                            timestamp TEXT NOT NULL,
                            FOREIGN KEY(datasource_id) REFERENCES datasources(id)
                        )''')

    def add_test_run(self, test_run: TestRunType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO test_runs (datasource_id, description, timestamp)
                                        VALUES (?, ?, ?)''', (test_run.datasource_id, test_run.description, test_run.timestamp))
            return cursor.lastrowid

    def add_or_get_test_run(self, test_run: TestRunType):
        cursor = self.db.execute('''SELECT * FROM test_runs WHERE description = ?''', (test_run.description,))
        row = cursor.fetchone()
        if row:
            return TestRunType.from_tuple(row)
        else:
            test_run.id = self.add_test_run(test_run)
            return test_run

    def get_test_run_by_id(self, id):
        cursor = self.db.execute('''SELECT * FROM test_runs WHERE id = ?''', (id,))
        row = cursor.fetchone()
        return TestRunType.from_tuple(row) if row else None

    def get_test_runs_by_datasource_id(self, datasource_id):
        cursor = self.db.execute('''SELECT * FROM test_runs WHERE datasource_id = ?''', (datasource_id,))
        return [TestRunType.from_tuple(row) for row in cursor.fetchall()]

    def get_test_run_by_name(self, description):
        cursor = self.db.execute('''SELECT * FROM test_runs WHERE description = ?''', (description,))
        row = cursor.fetchone()
        return TestRunType.from_tuple(row) if row else None