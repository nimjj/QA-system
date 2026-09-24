import os
import json
import urllib.request
import urllib.error
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SERVER_PORT = os.getenv("SERVER_PORT", "8000")
API_EVALUATE_URL = os.getenv("API_EVALUATE_URL", f"http://localhost:{SERVER_PORT}/api/evaluate")
INPUT_DIR = "inputs"
OUTPUT_DIR = "inputs/Test (results)"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    json_files = [f for f in sorted(os.listdir(INPUT_DIR)) if f.endswith('.json')]
    if not json_files:
        print(f"No JSON files found in '{INPUT_DIR}' directory.")
        return

    print(f"Found {len(json_files)} files. Starting batch run...\n")

    for idx, filename in enumerate(json_files, 1):
        filepath = os.path.join(INPUT_DIR, filename)
        print(f"[{idx}/{len(json_files)}] Processing: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                payload = json.load(f)
                
            req_data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                API_EVALUATE_URL,
                data=req_data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                result_data = json.loads(resp.read().decode('utf-8'))

            status = result_data.get("status", "completed")
            final_score = result_data.get("result", {}).get("final_score")
            print(f"  -> [{status.upper()}] Final Score: {final_score}")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"result_{timestamp}_{filename}"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as out_f:
                json.dump(result_data, out_f, indent=2)
                
            print(f"  -> Saved result to: {output_path}\n")
                
        except Exception as e:
            print(f"  -> EXCEPTION: {str(e)}\n")

if __name__ == "__main__":
    main()
