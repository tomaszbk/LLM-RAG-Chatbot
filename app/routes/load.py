import io
from datetime import datetime

from fastapi import APIRouter, File, UploadFile
from pypdf import PdfReader

from app.infrastructure.document_db import insert_document
from app.infrastructure.vector_db import store_embedding
from app.services.embedding_model import get_sentence_embedding
from app.services.splitter import text_splitter

router = APIRouter()


@router.post("/pdf-document")
async def submit_pdf_document(file: UploadFile = File(...)):
    filename = "pdf_document" if file.filename is None else file.filename

    contents = await file.read()
    file_like_object = io.BytesIO(contents)
    pdf_reader = PdfReader(file_like_object)
    pdf_content = pdf_reader.pages[0].extract_text()
    chunks = text_splitter.split_text(pdf_content)
    for i, chunk in enumerate(chunks):
        chunk = chunk.replace("\n", " ")
        id = insert_document(title=filename + f"-{i}", content=chunk)
        embedding = get_sentence_embedding(chunk)
        store_embedding(embedding, str(id))
    return {"message": "Document submitted successfully"}


@router.post("/text")
async def submit_text(text: str):
    chunks = text_splitter.split_text(text)
    now = datetime.now()
    for i, chunk in enumerate(chunks):
        chunk = chunk.replace("\n", " ")
        id = insert_document(title="text" + f"-{now}-{i}", content=chunk)
        embedding = get_sentence_embedding(chunk)
        store_embedding(embedding, str(id))
    return {"message": "Document submitted successfully"}
