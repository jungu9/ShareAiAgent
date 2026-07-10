from chromadb import PersistentClient
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)


class RagExecutor:

    def __init__(self):

        embedding = SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        client = PersistentClient(path="./chromadb")

        self._collection = client.get_collection(
            name="mes_schema",
            embedding_function=embedding,
        )

    def search_schema(
        self,
        question: str,
        top_k: int = 5,          # 가장 관련도 높은 문서 5개 반환 
    ) -> list[str]:

        result = self._collection.query(
            query_texts=[question],
            n_results=top_k,
        )

        return result["documents"][0]
