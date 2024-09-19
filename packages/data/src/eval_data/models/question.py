from typing import Optional

class QuestionType:
    id: Optional[int]
    qaset_id: int
    document_id: int
    question: str
    answer: str

    def __init__(self, qaset_id: int, document_id: int, question: str, answer: str, id: int = None):
        self.id = id
        self.qaset_id = qaset_id
        self.document_id = document_id
        self.question = question
        self.answer = answer

    def to_dict(self):
        return {
            'id': self.id,
            'qaset_id': self.qaset_id,
            'document_id': self.document_id,
            'question': self.question,
            'answer': self.answer
        }

    @staticmethod
    def from_dict(data: dict):
        return QuestionType(
            id=data.get('id'),
            qaset_id=data.get('qaset_id'),
            document_id=data.get('document_id'),
            question=data.get('question'),
            answer=data.get('answer')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        return QuestionType(
            id=data[0],
            qaset_id=data[1],
            document_id=data[2],
            question=data[3],
            answer=data[4]
        )

class QuestionModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS questions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            qaset_id INTEGER NOT NULL,
                            document_id INTEGER NOT NULL,
                            question TEXT NOT NULL,
                            answer TEXT NOT NULL,
                            FOREIGN KEY(qaset_id) REFERENCES qasets(id),
                            FOREIGN KEY(document_id) REFERENCES documents(id)
                        )''')

    def add_question(self, question: QuestionType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO questions (qaset_id, document_id, question, answer)
                                        VALUES (?, ?, ?, ?)''', (question.qaset_id, question.document_id, question.question, question.answer))
            return cursor.lastrowid

    def get_question_by_id(self, question_id):
        cursor = self.db.execute('''SELECT * FROM questions WHERE id = ?''', (question_id,))
        if row := cursor.fetchone():
            return QuestionType.from_tuple(row)
        else:
            return None
        
    def get_questions_by_qaset_id(self, qaset_id):
        cursor = self.db.execute('''SELECT * FROM questions WHERE qaset_id = ?''', (qaset_id,))
        questions = [QuestionType.from_tuple(row) for row in cursor.fetchall()]
        return questions

    def get_questions_by_document_id(self, document_id):
        cursor = self.db.execute('''SELECT * FROM questions WHERE document_id = ?''', (document_id,))
        questions = [QuestionType.from_tuple(row) for row in cursor.fetchall()]
        return questions

    def update_question(self, question: QuestionType):
        with self.db:
            cursor = self.db.execute('''UPDATE questions SET qaset_id = ?, document_id = ?, question = ?, answer = ? WHERE id = ?''',
                            (question.qaset_id, question.document_id, question.question, question.answer, question.id))
            return cursor.rowcount > 0

    def delete_question(self, question_id):
        with self.db:
            cursor = self.db.execute('''DELETE FROM questions WHERE id = ?''', (question_id,))
            return cursor.rowcount > 0

