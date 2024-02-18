from loguru import logger
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.infrastructure.document_db import retrieve_contexts
from app.infrastructure.vector_db import collection, retrieve_context_ids
from app.services.conversational_model import get_conversational_answer
from app.services.embedding_model import get_sentence_embedding

prompt_with_context_template = """Answer only the following QUESTION based on the CONTEXT given.


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


def transform_embedding_to_str(embedding):
    new_list = []
    return new_list.append(str(list(embedding)))


def generate_conversational_answer(prompt: str, session, use_rag: bool = True):
    if use_rag:
        question_embedding = get_sentence_embedding(prompt)
        context_ids: list = retrieve_context_ids(question_embedding, session)
        context = retrieve_contexts(context_ids[0], session)
        if context is not None:
            f_prompt = prompt_with_context_template.format(context=context, question=prompt)
        else:
            f_prompt = prompt_without_context_template.format(question=prompt)
    else:
        f_prompt = prompt_without_context_template.format(question=prompt)

    logger.info(f"F_PROMPT: {f_prompt}")
    return get_conversational_answer(f_prompt)
