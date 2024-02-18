from sqlmodel import Session, SQLModel, create_engine, select

from app.infrastructure.models import Document

engine = create_engine("sqlite:///database/document_db.db")

# SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def insert_document(title: str, content: str):
    with Session(engine) as session:
        document = Document(title=title, content=content)
        session.add(document)
        session.commit()
        return document.id


def retrieve_contexts(context_id: list, session: Session):
    query = select(Document).where(Document.id == context_id)
    result = session.exec(query).first()
    if result is not None:
        return result.content
    return result
