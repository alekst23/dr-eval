import pickle

class EvalFunctionType:
    """ Represents an evaluation function. """
    def __init__(self, name: str, description: str, eval_function: bytes, id: int=None):
        self.id = id
        self.name = name
        self.description = description
        self.eval_function = eval_function

    def to_dict(self):
        """ Converts the eval function object to a dictionary. """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'eval_function': self.eval_function
        }

    @staticmethod
    def from_dict(data: dict):
        """ Creates an eval function object from a dictionary. """
        return EvalFunctionType(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            eval_function=data.get('eval_function')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        """ Creates an eval function object from a tuple. """
        return EvalFunctionType(
            id=data[0],
            name=data[1],
            description=data[2],
            eval_function=pickle.loads(data[3])
        )

class EvalFunctionModel:
    """ Handles database operations for evaluation functions. """
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        """ Creates the eval_functions table in the database if it does not exist. """
        self.db.execute('''CREATE TABLE IF NOT EXISTS eval_functions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT NOT NULL,
                            eval_function BLOB NOT NULL
                        )''')

    def add_eval_function(self, eval_function: EvalFunctionType):
        """ Adds a new eval function to the database. """
        serialized_blob = pickle.dumps(eval_function.eval_function)
        with self.db:
            cursor = self.db.execute('''INSERT INTO eval_functions (name, description, eval_function)
                                        VALUES (?, ?, ?)''', (eval_function.name, eval_function.description, serialized_blob))
            return cursor.lastrowid

    def get_eval_function_by_id(self, eval_function_id: int):
        """ Retrieves an eval function from the database by its ID. """
        cursor = self.db.execute('SELECT * FROM eval_functions WHERE id = ?', (eval_function_id,))
        data = cursor.fetchone()
        if data:
            return EvalFunctionType.from_tuple(data)
        return None
    
    def get_eval_function_by_name(self, name: str):
        """ Retrieves an eval function from the database by its name. """
        cursor = self.db.execute('SELECT * FROM eval_functions WHERE name = ?', (name,))
        data = cursor.fetchone()
        if data:
            return EvalFunctionType.from_tuple(data)
        return None
    
    def add_or_get_eval_function(self, eval_function: EvalFunctionType):
        """ Adds a new eval function to the database if it does not exist, otherwise retrieves the existing eval function. """
        existing_eval_function = self.get_eval_function_by_name(eval_function.name)
        if existing_eval_function:
            return existing_eval_function
        else:
            eval_function.id = self.add_eval_function(eval_function)
            return eval_function
            

    def update_eval_function(self, eval_function: EvalFunctionType):
        """ Updates an existing eval function in the database. """
        serialized_blob = pickle.dumps(eval_function.eval_function)
        with self.db:
            cursor = self.db.execute('''UPDATE eval_functions
                                SET name = ?, description = ?, eval_function = ?
                                WHERE id = ?''', (eval_function.name, eval_function.description, serialized_blob, eval_function.id))
            return cursor.rowcount > 0

    def delete_eval_function(self, eval_function_id: int):
        """ Deletes an eval function from the database by its ID. """
        with self.db:
            self.db.execute('DELETE FROM eval_functions WHERE id = ?', (eval_function_id,))
            return True

    def get_all_eval_functions(self):
        """ Retrieves all eval functions from the database. """
        cursor = self.db.execute('SELECT * FROM eval_functions')
        return [EvalFunctionType.from_tuple(row) for row in cursor.fetchall()]
