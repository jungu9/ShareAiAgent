from app.executors.query import QueryRequestDto
from app.dtos.query import QueryResponseDto

from app.executors.query import LlmExecutor

from app.prompts.query import (
    SYSTEM_PROMPT,
    build_prompt,
)

from app.repositories.query import SchemaRepository


class QueryService:

    def __init__(
        self,
        connection_string: str,
        model: str = "qwen3:8b",
    ):
        self._schema_repository = SchemaRepository(connection_string)
        self._llm_executor = LlmExecutor(model=model)

    def generate_sql(
        self,
        request: QueryRequestDto,
    ) -> QueryResponseDto:
        """
        자연어 -> SQL 생성
        """

        # 1. DB 스키마 조회
        schema = self._schema_repository.get_schema_text()

        # 2. Prompt 생성
        prompt = build_prompt(
            question=request.question,
            schema=schema,
        )

        # 3. LLM 호출
        sql = self._llm_executor.generate_sql(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
        )

        # 4. 반환
        return QueryResponseDto(
            success=True,
            question=request.question,
            sql=sql,
            message="SQL generated successfully.",
        )