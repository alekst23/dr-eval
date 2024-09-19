import sqlite3
from datetime import datetime

class ResponseType:
    def __init__(self, test_run_id: int, question_id: int, response: str, timestamp: str = None, id: int = None):
        self.id = id
        self.test_run_id = test_run_id
        self.question_id = question_id
        self.response = response
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'id': self.id,
            'test_run_id': self.test_run_id,
            'question_id': self.question_id,
            'response': self.response,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(data: dict):
        return ResponseType(
            id=data.get('id'),
            test_run_id=data.get('test_run_id'),
            question_id=data.get('question_id'),
            response=data.get('response'),
            timestamp=data.get('timestamp')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        return ResponseType(
            id=data[0],
            test_run_id=data[1],
            question_id=data[2],
            response=data[3],
            timestamp=data[4]
        )

class ResponseModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS responses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            test_run_id INTEGER NOT NULL,
                            question_id INTEGER NOT NULL,
                            response TEXT NOT NULL,
                            timestamp TEXT NOT NULL,
                            FOREIGN KEY(test_run_id) REFERENCES test_runs(id),
                            FOREIGN KEY(question_id) REFERENCES questions(id)
                        )''')

    def add_response(self, response: ResponseType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO responses (test_run_id, question_id, response, timestamp)
                                        VALUES (?, ?, ?, ?)''', (response.test_run_id, response.question_id, response.response, response.timestamp))
            return cursor.lastrowid

    def get_responses_by_test_run_id(self, test_run_id):
        cursor = self.db.execute('''SELECT * FROM responses WHERE test_run_id = ?''', (test_run_id,))
        return [ResponseType.from_tuple(row) for row in cursor.fetchall()]

    def get_responses_by_question_id(self, question_id):
        cursor = self.db.execute('''SELECT * FROM responses WHERE question_id = ?''', (question_id,))
        return [ResponseType.from_tuple(row) for row in cursor.fetchall()]

