from pymongo import MongoClient

class NoDatabaseError(Exception):
    """Exception Raised when a database connection is not set"""

    def __init__(self, message="Database not defined"):
        self.message = message
        super().__init__(self.message)

class Mongo:
    """MongoDB connection constructor"""

    def __init__(self, host: str, username: str, password: str, authSource: str, **kwargs):
        """
        Args:
            host (str): hostname
            username (str): username to connect to Mongo
            password (str): password for authentication
            authSource (str): authentication source to use
            **kwargs (dict): passes into MongoClient
        """
        self.client = MongoClient(host=host, 
                                    username=username, 
                                    password=password, 
                                    authSource=authSource,
                                    **kwargs)
        self.db = None
        self.collection = None

    def set_db(self, key: str):
        """Set the database to access. Resets the collection to access"""
        self.db = self.client[key]
        self.collection = None
        return self

    def set_collection(self, key: str):
        """Set the collection to access. Requires a database to be set"""
        if self.db is None:
            raise NoDatabaseError()
        self.collection = self.db[key]
        return self

