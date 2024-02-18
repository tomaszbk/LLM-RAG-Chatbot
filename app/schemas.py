import pydantic


class Prompt(pydantic.BaseModel):
    prompt: str
