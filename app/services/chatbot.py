from sqlalchemy import text
from sqlalchemy.orm import Session
from app.services.conversational_model import get_conversational_answer
from app.services.embedding_model import get_sentence_embedding
from loguru import logger


prompt_with_context_template = """Answer only the following QUESTION based on the CONTEXT given.
do not continue the conversation further.
you can lie a little.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

prompt_without_context_template = """Answer only the following QUESTION.
do not continue the conversation further.

QUESTION:
{question}

ANSWER:
"""


def retrieve_context(p_embedding, session: Session) -> list:
    p_embedding = transform_embedding_to_str(p_embedding)
    query = text("""
        SELECT * FROM business_embeddings ORDER BY :p_embedding <-> embedding LIMIT 2;
    """)
    result = session.execute(query, dict(p_embedding= p_embedding)).fetchall()
    return result


def transform_embedding_to_str(embedding):
    new_list = []
    return new_list.append(str(list(embedding)))


def generate_bot_answer(question: str, session, use_rag: bool = True):
    if use_rag:
        question_embedding = get_sentence_embedding(question)
        context: list = retrieve_context(question_embedding, session)
        context = context[0][2]
        prompt = prompt_with_context_template.format(context=context, question=question)
    else:
        prompt = prompt_without_context_template.format(question=question)

    logger.info(f"PROMPT: {prompt}")
    return get_conversational_answer(question, prompt)
