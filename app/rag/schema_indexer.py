from chromadb import PersistentClient
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)


CHROMA_PATH = "./chromadb"
COLLECTION_NAME = "mes_schema"

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)

# 기존 데이터 삭제(테스트용)
result = collection.get()

if result["ids"]:
    collection.delete(ids=result["ids"])
    
# --------------------------------------------------------------------
# 품목마스터
# --------------------------------------------------------------------

biitm01t = """
Table : biitm01t
Description : 품목기본정보

Primary Key
- itemcd

Columns

itemcd : 품목코드
itemnm : 품명
itemkind : 품목계정
itemgbn1 : 품목분류1
itemgbn2 : 품목분류2
itemgbn3 : 품목분류3
itemgbn4 : 품목분류4
itemgbn5 : 품목분류5
prockind : 조달구분
pjtcd : 모델
spec : 규격
material : 재질
color : 색상
grade : 등급
unit : 단위
weight : 총중량
netweight : 런너중량
sprueweight : 스프루중량
cycletime : 사이클타임
tacttm : 택트타임
st : 표준시간
moldcd : 금형코드
moldseq : 금형차수
status : 상태
lotyn : LOT수불여부
remark : 비고
"""

# --------------------------------------------------------------------
# 작업지시
# --------------------------------------------------------------------

mpwod01t = """
Table : mpwod01t
Description : 작업지시

Primary Key
- wordno

Columns

wordno : 작업지시번호
workdt : 작업일자
workseq : 작업순번
workcd : 설비라인코드
status : 작업상태
shift : 근무조
itemcd : 품목코드
lotno : LOT번호
goalqty : 목표수량
planqty : 지시수량
workqty : 실적수량
goodqty : 양품수량
badqty : 불량수량
matqty : 원료사용량
worker : 작업자
supervisor : 책임자
realsttm : 실제시작일시
realtotm : 실제종료일시
remark : 비고
"""

collection.add(
    ids=[
        "schema_biitm01t",
        "schema_mpwod01t",
    ],
    documents=[
        biitm01t,
        mpwod01t,
    ],
    metadatas=[
        {
            "table": "biitm01t",
            "description": "품목기본정보",
        },
        {
            "table": "mpwod01t",
            "description": "작업지시",
        },
    ],
)

print("========================================")
print("Schema Index Complete")
print("Collection :", COLLECTION_NAME)
print("Documents  :", collection.count())
print("========================================")



# 실행 명령어: python app/rag/schema_indexer.py