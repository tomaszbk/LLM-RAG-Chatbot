from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker
from loguru import logger

from app.config import get_vector_db_uri


class VectorDBSessionFactory:
    def __init__(self) -> None:
        self.engine = create_engine(get_vector_db_uri())
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        session = self.Session()
        try:
            logger.info("session created")
            yield session
        finally:
            logger.info("session closed")
            session.close()


vector_db_session_factory = VectorDBSessionFactory()