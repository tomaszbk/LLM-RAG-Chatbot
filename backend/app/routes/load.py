from app.infrastructure.vector_db import collection, store_documents
from app.services.llm_model import get_multiple_sentence_embeddings
from app.services.splitter import text_splitter
from fastapi import APIRouter

router = APIRouter()


@router.post("/text")
async def submit_text(text: str):
    chunks = text_splitter.split_text(text)
    embeddings = []
    for chunk in chunks:
        chunk = chunk.replace("\n", " ")
    embeddings.append(get_multiple_sentence_embeddings(chunks))
    store_documents(collection, chunks, embeddings, [str(i) for i in range(len(chunks))])
    return {"message": "Document submitted successfully"}
