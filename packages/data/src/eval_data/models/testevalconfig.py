
class TestEvalConfigType:
    """ Represents a test evaluation configuration. """
    def __init__(self, test_run_id: int, eval_function_id: int, id: int=None):
        self.id = id
        self.test_run_id = test_run_id
        self.eval_function_id = eval_function_id

    def to_dict(self):
        """ Converts the test eval config object to a dictionary. """
        return {
            'id': self.id,
            'test_run_id': self.test_run_id,
            'eval_function_id': self.eval_function_id
        }

    @staticmethod
    def from_dict(data: dict):
        """ Creates a test eval config object from a dictionary. """
        return TestEvalConfigType(
            id=data.get('id'),
            test_run_id=data.get('test_run_id'),
            eval_function_id=data.get('eval_function_id')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        """ Creates a test eval config object from a tuple. """
        return TestEvalConfigType(
            id=data[0],
            test_run_id=data[1],
            eval_function_id=data[2]
        )

class TestEvalConfigModel:
    """ Handles database operations for test evaluation configurations. """
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        """ Creates the test_eval_configs table in the database if it does not exist. """
        self.db.execute('''CREATE TABLE IF NOT EXISTS test_eval_configs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            test_run_id INTEGER NOT NULL,
                            eval_function_id INTEGER NOT NULL,
                            FOREIGN KEY(test_run_id) REFERENCES test_runs(id),
                            FOREIGN KEY(eval_function_id) REFERENCES eval_functions(id)
                        )''')

    def add_test_eval_config(self, test_eval_config: TestEvalConfigType):
        """ Adds a new test eval config to the database. """
        with self.db:
            cursor = self.db.execute('''INSERT INTO test_eval_configs (test_run_id, eval_function_id)
                                        VALUES (?, ?)''', (test_eval_config.test_run_id, test_eval_config.eval_function_id))
            return cursor.lastrowid

    def get_test_eval_config_by_id(self, test_eval_config_id):
        """ Retrieves a test eval config from the database by its ID. """
        cursor = self.db.execute('SELECT * FROM test_eval_configs WHERE id = ?', (test_eval_config_id,))
        return TestEvalConfigType.from_tuple(cursor.fetchone())

    def get_test_eval_configs_by_test_run_id(self, test_run_id):
        """ Retrieves all test eval configs from the database by test run ID. """
        cursor = self.db.execute('SELECT * FROM test_eval_configs WHERE test_run_id = ?', (test_run_id,))
        return [TestEvalConfigType.from_tuple(row) for row in cursor.fetchall()]
