from pydantic import BaseModel


class QueryRequestDto(BaseModel):
    question: str