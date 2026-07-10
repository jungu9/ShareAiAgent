from app.executors.rag_executor import RagExecutor

rag = RagExecutor()

result = rag.search_schema(
    "2026년 7월 10일에 작업한 작업지시번호들이 궁금해"
)

print("====================")

for doc in result:
    print(doc)
    print("--------------------")


# 실행명령어: python -m test.test