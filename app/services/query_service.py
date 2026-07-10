from app.dtos.query_request_dto import QueryRequestDto
from app.dtos.query_response_dto import QueryResponseDto

from app.executors.llm_executor import LlmExecutor
from app.executors.rag_executor import RagExecutor

from app.prompts.sql_prompt import (
    SYSTEM_PROMPT,
    build_prompt,
)


class QueryService:

    def __init__(
        self,
        model: str = "qwen3:8b",
    ):
        self._rag_executor = RagExecutor()
        self._llm_executor = LlmExecutor(model=model)

    def generate_sql(
        self,
        request: QueryRequestDto,
    ) -> QueryResponseDto:

        schema = self._rag_executor.search_schema(
            request.question
        )

        prompt = build_prompt(
            question=request.question,
            schema=schema,
        )

        sql = self._llm_executor.generate_sql(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
        )

        return QueryResponseDto(
            success=True,
            question=request.question,
            sql=sql,
            message="success",
        )