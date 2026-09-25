# Marketing Workspace

## Status & Boundaries
- **Scope:** Samostatný dedikovaný workspace pro Marketing.
- **Izolace:** Striktní oddělení od ostatních repozitářů/projektů.
- **Git Policy:** Propojeno a synchronizováno s privátním remote repo: `https://github.com/ImperialBohemia/Marketing.git`.
- **Dokumentace:** Zápis všech pravidel, architektury, zjištění a logiky do lokálních `.md` souborů a verzováno v repozitáři.

---

## Sklik Production Integration (Permanent Access)
Workspace má nakonfigurovaný trvalý přístup k oběma API rozhraním Skliku (Drak + Fénix Admin) bez nutnosti dohledávat klíče.

- **Konfigurace a klíče:** [`.env.sklik`](file:///home/q/Marketing/.env.sklik)
- **Unifikovaný Python & CLI klient:** [`sklik_tool.py`](file:///home/q/Marketing/sklik_tool.py)
- **Token Cache:** [`.sklik_cache.json`](file:///home/q/Marketing/.sklik_cache.json) (automatická obnova Drak session a Fénix Bearer tokenu)

### Účet & Měření (SEM):
- **Uživatel:** `horoskopie.cz@email.cz` (User ID: `697549`)
- **Fénix Scopes:** Full admin (`sem`, `sem_id`, `sem_edit`, `sem_activate`, `campaign*`, `group*`, `ad*`, `conversion*`, `retargeting*`)
- **Public SEM ID (Frontend / GTM):** `hmaf4eme3mgcuspokyh7dpoc`
- **Private SEM ID (Backend S2S):** `hmaf4emdzae5zzlv6066wilt`
- **Aktivní konverze:** `CompleteRegistration` (ID: `100289271`, hodnota: 10 Kč)

### Rychlé příkazy v terminálu:
```bash
# Stav účtu, kredit a živé kampaně:
python3 sklik_tool.py status

# Výpis aktivních kampaní, sestav nebo inzerátů:
python3 sklik_tool.py campaigns
python3 sklik_tool.py groups
python3 sklik_tool.py keywords

# Návrhy klíčových slov a hledanost z databáze Seznamu:
python3 sklik_tool.py suggest "obytný přívěs"

# Přímá volání Drak / Fénix:
python3 sklik_tool.py drak <method_name> '[params]'
python3 sklik_tool.py fenix <METHOD> <path> '[body]'
```

### Použití v Python skriptech:
```python
from sklik_tool import sklik

# Volání Drak (PPC, klíčová slova, bidding)
res = sklik.drak("keywords.suggest", "tiny house", {"limit": 10})

# Volání Fénix (REST, SEM, Nákupy, obrázky)
res = sklik.fenix("GET", "/sklik/event-measurement/sem-id/")
```
