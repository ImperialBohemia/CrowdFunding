import json
import subprocess

def run_drak(method, params):
    cmd = ["python3", "scripts/seznam_tool.py", "drak", method, json.dumps(params)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except:
        return None

# We need to get all ads in the campaign 7977483
res = run_drak("campaigns.get", [{"id": 7977483}])
# Wait, campaigns.get doesn't return ads. We need ads.list. 
# We'll just fetch groups then ads, or just use the exact text replacements by searching.
