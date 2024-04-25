from app.infrastructure.vector_db import collection
from app.schemas import Prompt
from app.services.llm_model import get_conversational_answer
from app.services.rag import generate_conversational_rag_answer
from fastapi import APIRouter, File, UploadFile
from loguru import logger

router = APIRouter()


@router.post("/submit-prompt-rag")
def generate_rag_answer(prompt: Prompt):
    logger.info(f"PROMPT: {prompt.prompt}")

    output = generate_conversational_rag_answer(collection, prompt.prompt)
    return output


@router.post("/submit-prompt-rag-pdf")
async def generate_rag_answer_pdf(prompt: str, file: UploadFile = File(...)):
    logger.info(f"PROMPT: {prompt.prompt}")
    contents = await file.read()

    return generate_conversational_rag_answer(collection, prompt=prompt, file_content=contents)


@router.post("/submit-prompt")
def generate_answer(prompt: Prompt):
    logger.info(f"PROMPT: {prompt.prompt}")
    return get_conversational_answer(prompt.prompt)
