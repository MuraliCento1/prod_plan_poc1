import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "postgresql://postgres:799799@localhost:5432/postgres"

class Database:
    def __init__(self, database_url):
        """
        Initialize the Database class with the given database URL.
        Creates an engine and session maker.
        """
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self.metadata = MetaData()
        self.logger = logging.getLogger(__name__)

    def connect(self):
        """
        Connect to the database. Creates the engine and session maker.
        """
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.metadata.bind = self.engine  # Bind metadata to the engine
        self.logger.info("Database connection established.")

    def disconnect(self):
        """
        Disconnect from the database by disposing the engine.
        """
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.SessionLocal = None
            self.logger.info("Database connection closed.")

    def get_session(self):
        """
        Get a new database session.
        """
        if self.SessionLocal:
            return self.SessionLocal()
        else:
            self.logger.error("Database is not connected.")
            raise Exception("Database is not connected.")


