from utils.embedding_utils import EmbeddingModel
from vector_store.faiss_store import FAISSVectorStore
from mcp.protocol import create_mcp_message

class RetrievalAgent:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.vector_store = FAISSVectorStore()

    def process_documents(self, mcp_message):
        docs = mcp_message["payload"].get("documents", {})
        if not docs:
            print("⚠️ No documents found to embed.")
            return create_mcp_message(
                sender="RetrievalAgent",
                receiver="LLMResponseAgent",
                msg_type="RETRIEVAL_FAILED",
                payload={"error": "No documents received for retrieval."}
            )

        texts = list(docs.values())

        # 🔄 Clear old index to prevent repetition
        self.vector_store.reset()

        embeddings = self.embedder.embed_texts(texts)
        self.vector_store.add_texts(texts, embeddings)

        return create_mcp_message(
            sender="RetrievalAgent",
            receiver="LLMResponseAgent",
            msg_type="RETRIEVAL_READY",
            payload={"stored_docs": list(docs.keys())}
        )

    def retrieve(self, query):
        if not query or not query.strip():
            return create_mcp_message(
                sender="RetrievalAgent",
                receiver="LLMResponseAgent",
                msg_type="RETRIEVAL_FAILED",
                payload={"error": "Empty query provided."}
            )

        query_embedding = self.embedder.embed_texts([query])[0]
        top_chunks = self.vector_store.search(query_embedding, k=1)

        return create_mcp_message(
            sender="RetrievalAgent",
            receiver="LLMResponseAgent",
            msg_type="CONTEXT_RESPONSE",
            payload={"top_chunks": top_chunks, "query": query}
        )
