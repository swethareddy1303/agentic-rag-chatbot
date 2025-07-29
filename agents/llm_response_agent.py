from transformers import pipeline
from mcp.protocol import create_mcp_message

class LLMResponseAgent:
    def __init__(self):
        self.name = "LLMResponseAgent"
        self.qa_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base"
        )

    def generate_response(self, mcp_message):
        context_chunks = mcp_message["payload"].get("top_chunks", [])
        user_query = mcp_message["payload"].get("query", "")

        if not context_chunks or not user_query:
            return create_mcp_message(
                sender=self.name,
                receiver="User",
                msg_type="FINAL_RESPONSE",
                payload={"answer": "⚠️ Missing context or query."}
            )

        # Combine context and prompt the model
        context = "\n".join(context_chunks)
        prompt = f"Answer the question in 3-4 lines based on this context:\n{context}\nQuestion: {user_query}"

        result = self.qa_pipeline(prompt, max_length=200, do_sample=False)
        full_response = result[0]['generated_text'].strip()

        # Trim to last complete sentence (to prevent cutoff)
        if "." in full_response:
            trimmed_answer = full_response.rsplit(".", 1)[0] + "."
        else:
            trimmed_answer = full_response

        return create_mcp_message(
            sender=self.name,
            receiver="User",
            msg_type="FINAL_RESPONSE",
            payload={
                "answer": trimmed_answer,
                "full_context": context_chunks
            }
        )
