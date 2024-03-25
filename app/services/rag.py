from app.infrastructure.document_db import retrieve_contexts
from app.infrastructure.vector_db import retrieve_context_ids
from app.services.conversational_model import get_conversational_answer
from app.services.embedding_model import get_sentence_embedding


def generate_conversational_rag_answer(prompt: str, session):
    question_embedding = get_sentence_embedding(prompt)
    context_ids: list = retrieve_context_ids(question_embedding, session)
    context = retrieve_contexts(context_ids[0], session)

    return get_conversational_answer(prompt, context)
