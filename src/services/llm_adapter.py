import os
import json
import time
import urllib.request
import urllib.error

class BaseLLMAdapter:
    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError

class OllamaAdapter(BaseLLMAdapter):
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.url = f"{self.host.rstrip('/')}/api/chat"
        self.model = os.getenv("LLM_MODEL", "llama3.1")
        # Chat models (llama3.1, qwen) do not serve embeddings on this Ollama
        # server, so use a dedicated embedding model for the Vector Engine.
        self.embed_model = os.getenv("EMBED_MODEL", "nomic-embed-text")

    def generate(self, prompt: str, **kwargs) -> str:
        temperature = kwargs.get('temperature', 0.1)
        num_predict = kwargs.get('num_predict', 2048)
        num_ctx = kwargs.get('num_ctx', 8192)  # Max memory without crashing
        timeout = kwargs.get('timeout', 1800)
        
        payload_dict = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": num_predict, "num_ctx": num_ctx}
        }
        
        if kwargs.get('format') == 'json':
            payload_dict["format"] = "json"

        payload = json.dumps(payload_dict).encode("utf-8")

        # Retry transient failures / empty replies so a hiccup under load does not
        # silently become a wrong rating downstream.
        last_err = "empty reply"
        for attempt in range(4):
            req = urllib.request.Request(
                self.url, data=payload, headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = json.loads(resp.read())
                    content = data.get("message", {}).get("content", "").strip()
                    if content:
                        return content
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_err = exc
            time.sleep(2 * (attempt + 1))
        return f"Error reaching Ollama: {last_err}"

    def get_embedding(self, text: str, **kwargs) -> list[float]:
        url = f"{self.host.rstrip('/')}/api/embeddings"
        timeout = kwargs.get('timeout', 1800)
        
        payload_dict = {
            "model": self.embed_model,
            "prompt": text
        }

        payload = json.dumps(payload_dict).encode("utf-8")
        # Retry so an intermittent embedding failure does not become a false
        # Paraphrasing/Active-Listening FAIL (empty vector -> 0 similarity).
        for attempt in range(4):
            try:
                req = urllib.request.Request(
                    url, data=payload, headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = json.loads(resp.read())
                    emb = data.get("embedding", [])
                    if emb:
                        return emb
            except Exception as exc:
                last_err = exc
            time.sleep(2 * (attempt + 1))
        print("Embedding error: gave up after retries")
        return []

def get_llm() -> BaseLLMAdapter:
    # We could check env vars here to return different adapters (e.g., vLLMAdapter)
    return OllamaAdapter()


def query_llm(prompt, **kwargs):
    return get_llm().generate(prompt, **kwargs)

def get_embedding(text: str, **kwargs) -> list[float]:
    return get_llm().get_embedding(text, **kwargs)

def cache_prompt_prefix(prefix, **kwargs):
    return prefix

def query_llm_with_state(state, suffix, **kwargs):
    prompt = state + suffix
    return get_llm().generate(prompt, **kwargs)
