class TestEvalType:
    """ Represents a test evaluation. """
    def __init__(self, id: int, test_run_id: int):
        self.id = id
        self.test_run_id = test_run_id

    def to_dict(self):
        """ Converts the test eval object to a dictionary. """
        return {
            'id': self.id,
            'test_run_id': self.test_run_id
        }

    @staticmethod
    def from_dict(data: dict):
        """ Creates a test eval object from a dictionary. """
        return TestEvalType(
            id=data.get('id'),
            test_run_id=data.get('test_run_id')
        )

class TestEvalModel:
    """ Handles database operations for test evaluations. """
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        """ Creates the test_evals table in the database if it does not exist. """
        self.db.execute('''CREATE TABLE IF NOT EXISTS test_evals (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            test_run_id INTEGER NOT NULL,
                            FOREIGN KEY(test_run_id) REFERENCES test_runs(id)
                        )''')

    def add_test_eval(self, test_eval: TestEvalType):
        """ Adds a new test eval to the database. """
        with self.db:
            cursor = self.db.execute('''INSERT INTO test_evals (test_run_id)
                                        VALUES (?)''', (test_eval.test_run_id,))
            return cursor.lastrowid

    def get_test_evals_by_test_run_id(self, test_run_id):
        """ Retrieves all test evals from the database by test run ID. """
        cursor = self.db.execute('SELECT * FROM test_evals WHERE test_run_id = ?', (test_run_id,))
        return cursor.fetchall()

    def delete_test_eval(self, test_eval_id):
        """ Deletes a test eval from the database by test eval ID. """
        with self.db:
            self.db.execute('DELETE FROM test_evals WHERE id = ?', (test_eval_id,))

