# responseeval.py
# This module handles the response evaluation used in the application.

import sqlite3

class ResponseEvalType:
    """ Represents a response evaluation. """
    def __init__(self, test_run_id: int, question_id: int, response_id: int, test_eval_config_id: int, eval_score: float,  id: int = None):
        self.id = id
        self.test_run_id = test_run_id
        self.question_id = question_id
        self.response_id = response_id
        self.test_eval_config_id = test_eval_config_id
        self.eval_score = eval_score

    def to_dict(self):
        """ Converts the response eval object to a dictionary. """
        return {
            'id': self.id,
            'test_run_id': self.test_run_id,
            'question_id': self.question_id,
            'response_id': self.response_id,
            'test_eval_config_id': self.test_eval_config_id,
            'eval_score': self.eval_score
        }

    @staticmethod
    def from_dict(data: dict):
        """ Creates a response eval object from a dictionary. """
        return ResponseEvalType(
            id=data.get('id'),
            test_run_id=data.get('test_run_id'),
            question_id=data.get('question_id'),
            response_id=data.get('response_id'),
            test_eval_config_id=data.get('test_eval_config_id'),
            eval_score=data.get('eval_score')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        """ Creates a response eval object from a tuple. """
        return ResponseEvalType(
            id=data[0],
            test_run_id=data[1],
            question_id=data[2],
            response_id=data[3],
            test_eval_config_id=data[4],
            eval_score=data[5]
        )

class ResponseEvalModel:
    """ Handles database operations for response evaluations. """
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        """ Creates the response_evals table in the database if it does not exist. """
        self.db.execute('''CREATE TABLE IF NOT EXISTS response_evals (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            test_run_id INTEGER NOT NULL,
                            question_id INTEGER NOT NULL,
                            response_id INTEGER NOT NULL,
                            test_eval_config_id INTEGER NOT NULL,
                            eval_score REAL NOT NULL,
                            FOREIGN KEY(test_run_id) REFERENCES test_runs(id),
                            FOREIGN KEY(question_id) REFERENCES questions(id),
                            FOREIGN KEY(response_id) REFERENCES responses(id),
                            FOREIGN KEY(test_eval_config_id) REFERENCES test_eval_configs(id)
                        )''')

    def add_response_eval(self, response_eval: ResponseEvalType):
        """ Adds a new response eval to the database. """
        with self.db:
            cursor = self.db.execute('''INSERT INTO response_evals (test_run_id, question_id, response_id, test_eval_config_id, eval_score)
                                        VALUES (?, ?, ?, ?, ?)''', (response_eval.test_run_id, response_eval.question_id, response_eval.response_id, response_eval.test_eval_config_id, response_eval.eval_score))
            return cursor.lastrowid

    def get_response_evals_by_test_run_id(self, test_run_id):
        """ Retrieves all response evals from the database by test run ID. """
        cursor = self.db.execute('SELECT * FROM response_evals WHERE test_run_id = ?', (test_run_id,))
        return [ResponseEvalType.from_tuple(row) for row in cursor.fetchall()]

    def get_response_evals_by_question_id(self, question_id):
        """ Retrieves all response evals from the database by question ID. """
        cursor = self.db.execute('SELECT * FROM response_evals WHERE question_id = ?', (question_id,))
        return [ResponseEvalType.from_tuple(row) for row in cursor.fetchall()]

    def get_response_evals_by_response_id(self, response_id):
        """ Retrieves all response evals from the database by response ID. """
        cursor = self.db.execute('SELECT * FROM response_evals WHERE response_id = ?', (response_id,))
        return [ResponseEvalType.from_tuple(row) for row in cursor.fetchall()]

    def get_response_evals_by_test_eval_config_id(self, test_eval_config_id):
        """ Retrieves all response evals from the database by test eval config ID. """
        cursor = self.db.execute('SELECT * FROM response_evals WHERE test_eval_config_id = ?', (test_eval_config_id,))
        return [ResponseEvalType.from_tuple(row) for row in cursor.fetchall()]
