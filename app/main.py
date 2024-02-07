from fastapi import FastAPI
from fastapi import Depends

from app.models import Prompt
from app.services.chatbot import generate_bot_answer
from app.infrastructure.vector_db import vector_db_session_factory
from loguru import logger

app = FastAPI()


@app.post("/submit_prompt_rag")
def generate_rag_answer(prompt: Prompt, session=Depends(vector_db_session_factory.get_session)):
    logger.info("PROMPT:", prompt.prompt)
    return generate_bot_answer(prompt.prompt, use_rag=True, session=session)

@app.post("/submit_prompt")
def generate_answer(prompt: Prompt, session=Depends(vector_db_session_factory.get_session)):
    logger.info("PROMPT:", prompt.prompt)
    return generate_bot_answer(prompt.prompt, use_rag=False, session=session)