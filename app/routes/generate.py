from fastapi import APIRouter, Depends, File, UploadFile
from loguru import logger

from app.infrastructure.document_db import get_session
from app.schemas import Prompt
from app.services.conversational_model import get_conversational_answer
from app.services.rag import generate_conversational_rag_answer
from app.services.splitter import split_pdf

router = APIRouter()


@router.post("/submit-prompt-rag")
def generate_rag_answer(prompt: Prompt, session=Depends(get_session)):
    logger.info("PROMPT:", prompt.prompt)
    output = generate_conversational_rag_answer(prompt.prompt, session=session)
    return output


@router.post("/submit-prompt-rag-pdf")
async def generate_rag_answer_pdf(
    prompt: str, file: UploadFile = File(...), session=Depends(get_session)
):
    contents = await file.read()

    chunks = split_pdf(contents)
    return generate_conversational_rag_answer(prompt, session=session)


@router.post("/submit-prompt")
def generate_answer(prompt: Prompt, session=Depends(get_session)):
    logger.info("PROMPT:", prompt.prompt)
    return get_conversational_answer(prompt.prompt)
