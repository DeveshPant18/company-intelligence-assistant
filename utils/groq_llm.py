from langchain.llms.base import LLM
from pydantic import Field
import requests
from typing import Any, Dict
from config import GROQ_API_KEY

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

class GroqLLM(LLM):
    """LangChain LLM wrapper for Groq's Chat Completions API."""
    
    model: str = Field(default="llama3-70b-8192", description="Groq model name to use")

    def _call(self, prompt: str, stop=None) -> str:
        """Send the prompt to Groq API and return the text content."""
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a precise, citation-heavy company intelligence assistant. "
                        "Only use the provided context. Cite sources as [1], [2], ... and list URLs under 'Sources:'."
                    ),
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 700,
        }

        r = requests.post(GROQ_ENDPOINT, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()

        # Defensive parsing
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            if "choices" in data and data["choices"]:
                if "text" in data["choices"][0]:
                    return data["choices"][0]["text"]
            return f"[Unexpected Groq API response] {data}"

    # Helper methods for different LangChain calling styles
    def predict(self, text: str, **kwargs: Any) -> str:
        return self._call(text, stop=None)

    def invoke(self, input: Any, **kwargs: Any) -> str:
        return self._call(str(input), stop=None)

    def __call__(self, text: str, **kwargs: Any) -> str:
        return self._call(text, stop=None)

    @property
    def _llm_type(self) -> str:
        return "groq"

    def _identifying_params(self) -> Dict[str, Any]:
        return {"model": self.model}
