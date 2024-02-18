import io
from datetime import datetime

from fastapi import Depends, FastAPI, File, UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger
from pypdf import PdfReader

from app.infrastructure.document_db import get_session, insert_document
from app.infrastructure.vector_db import store_embedding
from app.schemas import Prompt
from app.services.chatbot import generate_conversational_answer
from app.services.embedding_model import get_sentence_embedding

app = FastAPI()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=350,  # 100 characters
    length_function=len,
)


@app.post("/submit-prompt-rag")
def generate_rag_answer(prompt: Prompt, session=Depends(get_session)):
    logger.info("PROMPT:", prompt.prompt)
    return generate_conversational_answer(prompt.prompt, use_rag=True, session=session)


@app.post("/submit-prompt")
def generate_answer(prompt: Prompt, session=Depends(get_session)):
    logger.info("PROMPT:", prompt.prompt)
    return generate_conversational_answer(prompt.prompt, use_rag=False, session=session)


@app.post("/pdf-document")
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


@app.post("/text")
async def submit_text(text: str):
    chunks = text_splitter.split_text(text)
    now = datetime.now()
    for i, chunk in enumerate(chunks):
        chunk = chunk.replace("\n", " ")
        id = insert_document(title="text" + f"-{now}-{i}", content=chunk)
        embedding = get_sentence_embedding(chunk)
        store_embedding(embedding, str(id))
    return {"message": "Document submitted successfully"}
