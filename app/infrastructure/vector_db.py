import chromadb
from chromadb.config import Settings
from sqlmodel import Session

db = chromadb.PersistentClient(path="./database", settings=Settings(anonymized_telemetry=False))

collection = db.get_or_create_collection(name="chatbot_data")


# TODO upload to trello thresshold task
def store_embedding(embedding, id: str):
    collection.add(
        embeddings=[embedding.tolist()],
        # documents=["This is a document"],
        # metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=[id],
    )


def store_embedding_with_document(embedding, id: str, document: str, collection=collection):
    collection.add(
        embeddings=[embedding.tolist()],
        documents=[document],
        # metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=[id],
    )


def retrieve_context(embedding, collection=collection) -> list:
    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=3,
    )
    return results


def retrieve_context_ids(embedding, session: Session) -> list:
    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=2,
    )
    return results["ids"][0]


def retrieve_from_temp_collection(content_chunks: list[str], prompt: str, session: Session) -> str:
    collection = db.create_collection(name="temp_collection")
    collection.add(documents=content_chunks, ids=[str(i) for i in range(len(content_chunks))])
    return "a"
