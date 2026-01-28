# app/services/llm_mock.py

class LLMMock:
    def generate(self, prompt: str) -> str:
        return f"[Mock LLM] Réponse simulée pour le prompt : {prompt}"
