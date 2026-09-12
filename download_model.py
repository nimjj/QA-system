import os
from huggingface_hub import hf_hub_download

MODEL_REPO = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
MODEL_FILE = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "models")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

print(f"Downloading {MODEL_FILE} from {MODEL_REPO}...")
try:
    path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE,
        local_dir=DOWNLOAD_DIR,
        local_dir_use_symlinks=False
    )
    print(f"Model successfully downloaded to: {path}")
except Exception as e:
    print(f"Failed to download model: {e}")

