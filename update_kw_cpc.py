import json
import subprocess
import time

def run_drak(method, params):
    cmd = ["python3", "scripts/seznam_tool.py", "drak", method, json.dumps(params)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except:
        return None

group_ids = [176710408, 176710888, 176710889, 176710890, 176710891, 176710845]

print("Fetching keywords...")
keywords_res = run_drak("keywords.list", [{"isDeleted": False}, {"limit": 100, "offset": 0}])

if keywords_res and "keywords" in keywords_res:
    kw_to_update = []
    for kw in keywords_res["keywords"]:
        if "group" in kw and kw["group"]["id"] in group_ids:
            kw_to_update.append({"id": kw["id"], "cpc": 100})
    
    if kw_to_update:
        print(f"Updating CPC for {len(kw_to_update)} keywords to 100 (1 CZK)...")
        print(run_drak("keywords.update", kw_to_update))
    else:
        print("No keywords found to update.")

