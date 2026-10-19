# CELL 4: download the English checkpoint at the pinned revision and compare it with the local copy.
# EXPECT: files listed (model.safetensors about 842 MB), "weights identical to local copy: True",
# "config identical to local copy: True", and max_len 512 / head_max_len 192.
from huggingface_hub import snapshot_download


def sha256_file(path, chunk=1 << 24):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


BASE = snapshot_download(BASE_REPO, revision=BASE_REV, local_dir=f"{WORK}/base-english",
                         allow_patterns=["model.safetensors", "rl_agent_config.json", "encoder/*", "tokenizer/*"])
for dp, _, fns in sorted(os.walk(BASE)):
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        if "/.cache" not in p.replace("\\", "/"):
            print(f"{os.path.getsize(p) / 1e6:9.1f} MB  {os.path.relpath(p, BASE)}")

BASE_SHA256 = {name: sha256_file(f"{BASE}/{name}") for name in LOCAL_BASE_SHA256}
same_w = BASE_SHA256["model.safetensors"] == LOCAL_BASE_SHA256["model.safetensors"]
same_c = BASE_SHA256["rl_agent_config.json"] == LOCAL_BASE_SHA256["rl_agent_config.json"]
print("weights identical to local copy:", same_w)
print("config identical to local copy:", same_c)
BASE_CFG = json.load(open(f"{BASE}/rl_agent_config.json"))
print("max_len", BASE_CFG["max_len"], "| head_max_len", BASE_CFG["head_max_len"], "| encoder", BASE_CFG["encoder"])
assert same_w and same_c, "downloaded base differs from the local snapshot: stop and tell Claude"
