import re

from ollama import Client


class LlmExecutor:
    """
    Ollama LLM 실행
    """

    def __init__(
        self,
        model: str = "qwen3:8b",
        host: str = "http://localhost:11434",
    ):
        self._model = model
        self._client = Client(host=host)

    def generate_sql(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        자연어 -> SQL 생성
        """

        response = self._client.chat(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            options={
                "temperature": 0,
            },
        )

        sql = response["message"]["content"]

        return self._clean_sql(sql)

    def _clean_sql(
        self,
        sql: str,
    ) -> str:
        """
        Ollama 응답 정리
        """

        sql = sql.strip()

        # ```sql 제거
        sql = re.sub(
            r"```sql",
            "",
            sql,
            flags=re.IGNORECASE,
        )

        sql = sql.replace("```", "")

        # 세미콜론 제거
        sql = sql.rstrip(";")

        return sql.strip()