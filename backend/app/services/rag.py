from app.infrastructure.vector_db import retrieve_documents, store_documents
from app.services.llm_model import (
    get_conversational_answer,
    get_multiple_sentence_embeddings,
    get_sentence_embedding,
)
from app.services.splitter import split_pdf


def generate_conversational_rag_answer(collection, prompt: str, file_content: bytes = None):
    question_embedding = get_sentence_embedding(prompt)

    if file_content:
        chunks = split_pdf(file_content)
        embeddings = []
        for chunk in chunks:
            chunk = chunk.replace("\n", " ")
        embeddings.append(get_multiple_sentence_embeddings(chunks))
        store_documents(collection, chunks, embeddings, [str(i) for i in range(len(chunks))])
    context = retrieve_documents(collection, question_embedding.tolist())
    if context["documents"][0][0]:
        context_str = ""
        for i in context["documents"][0]:
            context_str += i + " "
    else:
        context_str = None
    return get_conversational_answer(prompt, context_str)
