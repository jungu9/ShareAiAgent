import re

from ollama import Client


class LlmExecutor:

    def __init__(
        self,
        model: str = "qwen3:8b",
        host: str = "http://localhost:11434",
    ):
        self._client = Client(host=host)
        self._model = model

    def generate_sql(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

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

        sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
        sql = sql.replace("```", "")
        sql = sql.strip().rstrip(";")

        return sql