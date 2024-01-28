from fastapi import FastAPI
from fastapi import HTTPException, status, Depends


from app.services.chatbot import generate_bot_answer
from app.infrastructure.vector_db import vector_db_session_factory
from loguru import logger

app = FastAPI()


@app.post("/submit_prompt")
def generate_rag_answer(prompt: str,session=Depends(vector_db_session_factory.get_session)):
    logger.info("PROMPT:", prompt)
    return generate_bot_answer(prompt, use_rag=True, session=session)