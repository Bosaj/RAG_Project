import requests

from ..LLMInterface import LLMInterface


class OllamaProvider(LLMInterface):
    def __init__(self, model_name="llama3", host="http://127.0.0.1:11434"):
        self.model_name = model_name
        self.host = host

    def set_generation_model(self, model_id: str):
        self.model_name = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass

    def process_text(self, text: str):
        return text.strip()

    def generate_text(
        self,
        prompt: str,
        chat_history: list | None = None,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
    ):
        if chat_history is None:
            chat_history = []
        data = {
            "model": self.model_name,
            "prompt": self.process_text(prompt),
        }
        if max_output_tokens:
            data["num_predict"] = max_output_tokens
        if temperature:
            data["temperature"] = temperature
        try:
            response = requests.post(f"{self.host}/api/generate", json=data)
            response.raise_for_status()
            result = response.json()
            return result.get("response", None)
        except Exception:
            import traceback

            print("[OLLAMA ERROR] Exception while generating text:")
            traceback.print_exc()
            print(f"[OLLAMA ERROR] Data sent: {data}")
            print(f"[OLLAMA ERROR] Host: {self.host}")
            return None

    def embed_text(self, text: str, document_type: str | None = None):
        # L'embedding se fait via sentence-transformers, pas Ollama
        return None

    def construct_prompt(self, prompt: str, role: str):
        return {"role": role, "text": self.process_text(prompt)}
