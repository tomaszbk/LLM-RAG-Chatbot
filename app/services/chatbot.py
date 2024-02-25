from loguru import logger

from app.infrastructure.document_db import retrieve_contexts
from app.infrastructure.vector_db import retrieve_context_ids
from app.services.conversational_model import get_conversational_answer
from app.services.embedding_model import get_sentence_embedding

prompt_with_context_template = """You are a chatbot named kukebot. Answer the following QUESTION.
If you dont know the answer, reply: "I don't know".
CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

prompt_without_context_template = prompt_with_context_template.replace("CONTEXT:\n{context}\n", "")


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
