"""In-process LLM inference using llama-cpp-python.

Loads the K2 Horizon GGUF model directly into RAM to prevent network latency
and manage memory (KV cache) safely.
"""

import os
from llama_cpp import Llama

_LLM_INSTANCE = None

def get_llm():
    global _LLM_INSTANCE
    if _LLM_INSTANCE is None:
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models", "k2-horizon-3.7b-Q4_K_M.gguf")
        
        # Ensure the model exists before loading
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Run setup.bat or setup.sh to download it.")

        print(f"--- LOADING LOCAL MODEL INTO RAM ---")
        _LLM_INSTANCE = Llama(
            model_path=model_path,
            n_ctx=16384,      # ~30 minute transcript capacity (adjust to 8192 if running low on RAM)
            n_threads=8,      # Utilize vCPUs
            n_batch=512,
            verbose=False     # Set to True for memory allocation logs
        )
        print(f"--- MODEL SUCCESSFULLY LOADED ---")
    return _LLM_INSTANCE


def query_llm(prompt: str, label: str = None) -> str:
    """Execute inference directly in-process using llama-cpp-python."""
    llm = get_llm()
    
    # We use a lower max_tokens for scorecard parts, but keep it enough to not cut off
    output = llm(
        prompt,
        max_tokens=500,
        temperature=0.1,
        stop=["<|user|>"],
        echo=False
    )
    
    return output["choices"][0]["text"].strip()


def cache_prompt_prefix(prefix_text: str):
    """
    Ingest a massive prompt (like a transcript) once and return the KV Cache state.
    This prevents us from having to pass and re-tokenize the transcript for every map-reduce chunk.
    """
    llm = get_llm()
    tokens = llm.tokenize(prefix_text.encode("utf-8"))
    
    # Reset context and explicitly evaluate the prefix to fill the KV Cache
    llm.reset()
    llm.eval(tokens)
    
    # Save the internal C++ state (KV cache) to RAM
    return llm.save_state()


def query_llm_with_state(state, suffix_text: str, label: str = None) -> str:
    """
    Restore a previously saved KV Cache state (the transcript), 
    append the new chunk (the criteria), and generate the result.
    """
    llm = get_llm()
    
    # Restore the massive transcript KV Cache instantly
    llm.load_state(state)
    
    # Run the generation ONLY on the small suffix chunk
    output = llm(
        suffix_text,
        max_tokens=500,
        temperature=0.1,
        stop=["<|user|>"],
        echo=False
    )
    
    return output["choices"][0]["text"].strip()

