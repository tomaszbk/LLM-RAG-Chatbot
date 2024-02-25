from fastapi import APIRouter, Depends, File, UploadFile
from loguru import logger

from app.infrastructure.document_db import get_session
from app.schemas import Prompt
from app.services.chatbot import generate_conversational_answer
from app.services.splitter import split_pdf

router = APIRouter()


@router.post("/submit-prompt-rag")
def generate_rag_answer(prompt: Prompt, session=Depends(get_session)):
    logger.info("PROMPT:", prompt.prompt)
    output = generate_conversational_answer(prompt.prompt, use_rag=True, session=session)
    print(output)
    return output


@router.post("/submit-prompt-rag-pdf")
async def generate_rag_answer_pdf(
    prompt: str, file: UploadFile = File(...), session=Depends(get_session)
):
    contents = await file.read()

    chunks = split_pdf(contents)
    return generate_conversational_answer(prompt, use_rag=True, session=session)


@router.post("/submit-prompt")
def generate_answer(prompt: Prompt, session=Depends(get_session)):
    logger.info("PROMPT:", prompt.prompt)
    return generate_conversational_answer(prompt.prompt, use_rag=False, session=session)
