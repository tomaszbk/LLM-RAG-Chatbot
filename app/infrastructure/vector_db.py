import chromadb
from chromadb.config import Settings

db = chromadb.PersistentClient(path="./database", settings=Settings(anonymized_telemetry=False))

collection = db.get_or_create_collection(name="chatbot_data")


# TODO upload to trello thresshold task
def store_documents(collection, documents, embeddings, ids: list[str]):
    collection.add(
        embeddings=embeddings,
        documents=documents,
        ids=ids,
    )


def retrieve_documents(collection, embedding: list) -> list:
    results = collection.query(
        query_embeddings=embedding, n_results=3, include=["embeddings", "documents", "distances"]
    )
    return results
