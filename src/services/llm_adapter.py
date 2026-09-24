import os
import json
import time
import urllib.request
import urllib.error

class OllamaAdapter:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.url = f"{self.host.rstrip('/')}/api/chat"
        self.model = os.getenv("LLM_MODEL", "llama3.1")
        self.embed_model = os.getenv("EMBED_MODEL", "nomic-embed-text")

    def generate(self, prompt: str, **kwargs) -> str:
        temperature = kwargs.get('temperature', 0.1)
        num_predict = kwargs.get('num_predict', 2048)
        num_ctx = kwargs.get('num_ctx', 8192)
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
        return []

_adapter = OllamaAdapter()

def get_llm() -> OllamaAdapter:
    return _adapter

def query_llm(prompt, **kwargs):
    return _adapter.generate(prompt, **kwargs)

def get_embedding(text: str, **kwargs) -> list[float]:
    return _adapter.get_embedding(text, **kwargs)

def query_llm_with_state(state, suffix, **kwargs):
    return _adapter.generate(state + suffix, **kwargs)
