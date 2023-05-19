"""Code written by Jacquesne Jones unless otherwise specified."""


class BaseModel:
    """Abstract base class used for all database models.

    This class gives the model access to the database and session to create standard models for accessing
    and manipulating data in the database.
    """
    def __init__(self, database, query_type):
        self.database = database
        self.session = database.session
        self.query_type = query_type

    def get(self, key):
        """Gets an item by id"""
        if not self.query_type:
            return False
        else:
            return self.session.query(self.query_type).filter(self.query_type.id == key).one()
