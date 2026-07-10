SYSTEM_PROMPT = """
당신은 Microsoft SQL Server(MSSQL) SQL 전문가입니다.

규칙

1. 반드시 SELECT만 생성한다.
2. INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, EXEC 사용 금지
3. SQL 외에는 아무것도 출력하지 않는다.
4. ```sql 코드블록 사용 금지
5. 제공된 스키마만 사용한다.
6. 컬럼명을 추측하지 않는다.
7. MSSQL 문법만 사용한다.
"""


def build_prompt(
    question: str,
    schema: str,
) -> str:

    return f"""
### Database Schema

{schema}

----------------------

### User Question

{question}

----------------------

위 스키마만 사용하여 MSSQL SQL을 생성하세요.
"""