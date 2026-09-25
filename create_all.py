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

groups = [
    {"id": 176710888, "name": "Kauce na byt"},
    {"id": 176710889, "name": "Děti z Klokánku"},
    {"id": 176710890, "name": "Matka v nouzi"},
    {"id": 176710891, "name": "Znesnáze Brand"},
]

ad_templates = {
    "Kauce na byt": [
        ("Kauce na byt pro rodinu", "Pomozte nám s nájmem", "Přispějte na kauci, ať můžeme podepsat nájem a vzít si dcery domů z ústavu."),
        ("Vraťme děti z ubytovny", "Sbírka na kauci", "Jediná šance na návrat dětí je zaplatit kauci za byt. Pomozte nám darem."),
        ("Pomoc pro dcery", "Zaplaťme kauci za byt", "Soud vyžaduje vhodné bydlení. Kauce je to jediné, co nám brání být zase rodina."),
        ("Sbírka: Kauce na bydlení", "Transparentní účet", "Znesnáze21 garantuje účel sbírky. Dary půjdou na nájem a kauci za domov."),
        ("Chybí nám kauce na byt", "Pomozte vrátit děti", "Nemáme startovní kauci za byt. Vaše peníze vrátí Jolanku a Marušku domů.")
    ],
    "Děti z Klokánku": [
        ("Děti musí zpět z Klokánku", "Pomozte s bydlením", "Jolanka a Maruška pláčou. Pomozte nám sehnat finance na kauci bytu a vzít je domů."),
        ("Návrat dětí z domova", "Finanční sbírka", "Holčičkám chybí rodiče. Potřebujeme jen peníze na kauci, aby soud povolil návrat."),
        ("Záchrana z Klokánku", "Vraťme děti rodině", "Odloučení je trauma. Máme vyhlédnutý byt, ale chybí kauce. Darujte ještě dnes."),
        ("Pomozte dětem z domova", "Jolanka a Maruška", "Děti patří k rodičům. Vašich 500 Kč nám pomůže podepsat nájem a vzít je z Klokánku."),
        ("Sbírka: Návrat z Klokánku", "Kauce na nový domov", "Jediná překážka návratu je chybějící kauce za byt. Darujte a zachraňte rodinu.")
    ],
    "Matka v nouzi": [
        ("Matka v těžké nouzi", "Pomozte s kaucí", "Rodina přišla o střechu nad hlavou. Děti musely do ústavu. Darujte na novou kauci."),
        ("Pomoc pro matku s dětmi", "Vraťme jim domov", "Těžká situace rozdělila rodinu. Kauce na byt je jedinou cestou, jak mít děti zpět."),
        ("Solidarita s matkou v nouzi", "Finanční sbírka", "Peníze na kauci dělí matku od návratu jejich dvou dcer z Klokánku. Pomozte jí."),
        ("Krize rozdělila rodinu", "Darujte na kauci", "Matka bojuje o dcery. Soud vyžaduje stabilní byt, ale na kauci teď chybí finance."),
        ("Pomozte zachránit rodinu", "Matka samoživitelka", "Ztráta bydlení vedla k odebrání dětí. Váš dar pomůže matce vrátit rodinu k sobě.")
    ],
    "Znesnáze Brand": [
        ("Sbírka na Znesnáze21", "Pomozte vrátit děti", "Oficiální transparentní sbírka na Znesnáze21. Pomozte rodině zaplatit kauci bytu."),
        ("Nadační fond pomoci", "Sbírka: Návrat dětí", "Přispějte přes prověřenou platformu Znesnáze21. Částka jde na kauci za bydlení."),
        ("Znesnáze21: Pomozte rodině", "Kauce na bydlení", "Soud vrátil naději, chybí jen peníze na kauci. Podpořte sbírku přes Znesnáze21."),
        ("Sbírka Znesnáze21", "Jolanka a Maruška", "Transparentní sbírka pro rodiče, kteří bojují o návrat dcer z dětského domova."),
        ("Pomoc přes Znesnáze21", "Ověřená sbírka", "Vaše dary jsou v bezpečí a jdou přímo rodině. Pomozte jim získat kauci na byt.")
    ]
}

for g in groups:
    group_name = g["name"]
    group_id = g["id"]
    if group_name in ad_templates:
        ads_payload = []
        for (h1, h2, desc) in ad_templates[group_name]:
            ads_payload.append({
                "groupId": group_id,
                "headline1": h1,
                "headline2": h2,
                "description": desc,
                "finalUrl": "https://navratdetidomu.cz/"
            })
        print(f"Adding ads to {group_name}")
        res = run_drak("ads.create", ads_payload)
        print(res)
        time.sleep(1)

