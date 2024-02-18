from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(unique=False)
    content: str = Field()
