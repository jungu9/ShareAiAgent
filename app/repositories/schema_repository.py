from __future__ import annotations

from typing import Any

import pyodbc


class SchemaRepository:
    """
    SQL Server 스키마 조회 Repository

    - 테이블 목록 조회
    - 컬럼 목록 조회
    - LLM Prompt에 사용할 스키마 문자열 생성
    """

    def __init__(self, connection_string: str):
        self._conn_str = connection_string

    def _connect(self) -> pyodbc.Connection:
        return pyodbc.connect(self._conn_str)

    def get_tables(self) -> list[str]:
        sql = """
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE='BASE TABLE'
        ORDER BY TABLE_NAME
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)

            return [
                row.TABLE_NAME
                for row in cursor.fetchall()
            ]

    def get_columns(self, table_name: str) -> list[dict[str, Any]]:
        sql = """
        SELECT
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
        """

        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(sql, table_name)

            result: list[dict[str, Any]] = []

            for row in cursor.fetchall():

                result.append(
                    {
                        "column_name": row.COLUMN_NAME,
                        "data_type": row.DATA_TYPE,
                        "nullable": row.IS_NULLABLE,
                    }
                )

            return result

    def get_schema_text(self) -> str:
        """
        LLM Prompt용 스키마 문자열 생성

        예)

        Table : biitm01t
          - itemcd varchar
          - itemnm nvarchar

        Table : mpwod01t
          - wordno varchar
          ...
        """

        tables = self.get_tables()

        texts: list[str] = []

        for table in tables:

            texts.append(f"Table : {table}")

            columns = self.get_columns(table)

            for column in columns:

                texts.append(
                    f"  - {column['column_name']} ({column['data_type']})"
                )

            texts.append("")

        return "\n".join(texts)