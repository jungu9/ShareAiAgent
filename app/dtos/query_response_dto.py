from pydantic import BaseModel


class QueryResponseDto(BaseModel):
    success: bool
    question: str
    sql: str
    message: str