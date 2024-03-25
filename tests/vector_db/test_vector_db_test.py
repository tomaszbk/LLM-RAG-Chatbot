def test_vector_db():
    # Create a vector database

    import chromadb
    from chromadb.config import Settings

    from app.infrastructure.vector_db import retrieve_context, store_embedding_with_document
    from app.services.embedding_model import get_sentence_embedding
    from app.services.splitter import text_splitter

    db = chromadb.EphemeralClient(settings=Settings(anonymized_telemetry=False))
    db.delete_collection(name="test_collection")
    collection = db.get_or_create_collection(name="test_collection")
    with open("tests/ow.txt") as file:
        text = file.read()
    chunks = text_splitter.split_text(text)
    for i, chunk in enumerate(chunks):
        chunk = chunk.replace("\n", " ")
        embedding = get_sentence_embedding(chunk)
        store_embedding_with_document(embedding, str(i), chunk, collection=collection)

    prompt = "What is Overwatch 2?"
    embedding = get_sentence_embedding(prompt)
    store_embedding_with_document(embedding, "1", prompt, collection=collection)
    print(retrieve_context(embedding, collection=collection))
