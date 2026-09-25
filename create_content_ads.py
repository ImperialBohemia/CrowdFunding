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

groups = [176710845, 176710979]
ads = [
    ("Vraťme děti k rodině", "Z ubytovny zpět domů", "Rodiče bojují o dcery. Chybí jen kauce na byt, aby nám je soud vrátil. Pomozte."),
    ("Pomozte dcerám k rodině", "Kauce na nový domov", "Rodina z ubytovny prosí o pomoc. Kauce na byt vrátí dcery z Klokánku k rodičům."),
    ("Sbírka: Záchrana rodiny", "Jolanka a Maruška", "Holčičky pláčou v domově. Pomozte nám splnit podmínku soudu. Darujte přes Znesnáze."),
    ("Solidarita s rodinou", "Finanční pomoc", "Rozdělená rodina prosí o pomoc s kaucí na byt. Udělejte dobrý skutek a darujte šanci."),
    ("Pomozte vrátit děti", "Ověřená sbírka", "Vaše dary jsou v bezpečí a jdou přímo rodině v nouzi. Pomozte jim získat kauci.")
]

for gid in groups:
    payload = []
    for (h1, h2, desc) in ads:
        payload.append({
            "groupId": gid,
            "headline1": h1,
            "headline2": h2,
            "description": desc,
            "finalUrl": "https://navratdetidomu.cz/"
        })
    run_drak("ads.create", payload)
    time.sleep(1)

print("Done")
