from sqlmodel import Session, SQLModel, create_engine

from app.infrastructure.models import Document

engine = create_engine("sqlite:///database/document_db.db")

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)


def insert_document(title: str, content: str):
    with Session(engine) as session:
        document = Document(title=title, content=content)
        session.add(document)
        session.commit()
        return document.id
