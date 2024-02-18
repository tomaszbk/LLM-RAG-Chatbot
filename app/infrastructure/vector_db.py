import random

import chromadb
from chromadb.config import Settings
from loguru import logger
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlmodel import Session

from app.config import get_vector_db_uri

db = chromadb.PersistentClient(path="./database", settings=Settings(anonymized_telemetry=False))

collection = db.get_or_create_collection(name="chatbot_data")


def store_embedding(embedding, id: str):
    collection.add(
        embeddings=[embedding.tolist()],
        # documents=["This is a document"],
        # metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=[id],
    )


def retrieve_context_ids(embedding, session: Session) -> list:
    # embedding = transform_embedding_to_str(embedding)
    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=2,
    )
    return results["ids"][0]
