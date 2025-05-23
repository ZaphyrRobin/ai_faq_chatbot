from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
