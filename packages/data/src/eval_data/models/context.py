class ContextType:
    """ Represents a context associated with a response. """
    def __init__(self, response_id: int, text: str, similarity_score: float, sort_index: int = None, id: int = None):
        self.id = id
        self.response_id = response_id
        self.text = text
        self.similarity_score = similarity_score
        self.sort_index = sort_index or 0

    def to_dict(self):
        """ Converts the context object to a dictionary. """
        return {
            'id': self.id,
            'response_id': self.response_id,
            'text': self.text,
            'similarity_score': self.similarity_score,
            'sort_index': self.sort_index
        }

    @staticmethod
    def from_dict(data: dict):
        """ Creates a context object from a dictionary. """
        return ContextType(
            id=data.get('id'),
            response_id=data.get('response_id'),
            text=data.get('text'),
            similarity_score=data.get('similarity_score'),
            sort_index=data.get('sort_index', 0)  # Default sort_index to 0 if not provided
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        """ Creates a context object from a tuple. """
        if not data:
            return
        return ContextType(
            id=data[0],
            response_id=data[1],
            text=data[2],
            similarity_score=data[3],
            sort_index=data[4]
        )

class ContextModel:
    """ Handles database operations for context data. """
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        """ Creates the contexts table in the database if it does not exist. """
        self.db.execute('''CREATE TABLE IF NOT EXISTS contexts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            response_id INTEGER NOT NULL,
                            text TEXT NOT NULL,
                            similarity_score REAL NOT NULL,
                            sort_index INTEGER NOT NULL,
                            FOREIGN KEY(response_id) REFERENCES responses(id)
                        )''')

    def add_context(self, context: ContextType):
        """ Adds a new context to the database. """
        with self.db:
            cursor = self.db.execute('''INSERT INTO contexts (response_id, text, similarity_score, sort_index)
                                        VALUES (?, ?, ?, ?)''', (context.response_id, context.text, context.similarity_score, context.sort_index))
            return cursor.lastrowid

    def get_contexts_by_response_id(self, response_id):
        """ Retrieves all contexts from the database by response ID. """
        cursor = self.db.execute('SELECT * FROM contexts WHERE response_id = ? ORDER BY sort_index', (response_id,))
        rows = cursor.fetchall()
        return [ContextType.from_tuple(row) for row in rows]

