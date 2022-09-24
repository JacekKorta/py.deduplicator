from pydantic import BaseModel, HttpUrl


class Question(BaseModel):
    tags: list[str]
    is_answered: bool
    last_activity_date: int
    creation_date: int
    question_id: int
    link: HttpUrl
    title: str
    body: str
