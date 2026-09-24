#!/usr/bin/env python3
"""
Přímý vyhledávač a monitor pronájmů z Bezrealitky.cz (bez prostředníků a provizí).
Nevyžaduje žádné placené API ani Apify. Čte přímo data z live Apollo Cache Bezrealitky.
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def fetch_bezrealitky_rentals(location=None, max_price=None, min_surface=None, limit=20):
    params = {
        'offerType': 'PRONAJEM',
        'estateType': 'BYT',
        'currency': 'CZK'
    }
    if max_price:
        params['priceTo'] = max_price
    
    url = f"https://www.bezrealitky.cz/vyhledat?{urllib.parse.urlencode(params)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3'
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Chyba při stahování: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(html, 'html.parser')
    next_data_tag = soup.find('script', id='__NEXT_DATA__')
    if not next_data_tag or not next_data_tag.string:
        print("Chyba: __NEXT_DATA__ nenalezeno.", file=sys.stderr)
        return []

    try:
        data = json.loads(next_data_tag.string)
        cache = data.get('props', {}).get('pageProps', {}).get('apolloCache', {})
    except Exception as e:
        print(f"Chyba při parsování JSON: {e}", file=sys.stderr)
        return []

    adverts = [v for k, v in cache.items() if k.startswith('Advert:')]
    results = []

    for ad in adverts:
        addr = ad.get('address({"locale":"CS"})') or ad.get('address') or ''
        if isinstance(addr, dict):
            addr = f"{addr.get('street', '')}, {addr.get('city', '')}"
        
        # Filtrovat pouze české adresy (vyřadit německé importy)
        foreign = ['Braniborsko', 'Sasko', 'Bayern', 'Hamburg', 'Nordrhein', 'Baden', 'Hessen', 'Sachsen']
        if any(f in addr for f in foreign):
            continue
        
        # Filtr na lokalitu (pokud zadána)
        if location and location.lower() not in addr.lower():
            continue

        price = ad.get('price', 0)
        if max_price and price > int(max_price):
            continue

        surface = ad.get('surface', 0)
        if min_surface and surface < int(min_surface):
            continue

        charges = ad.get('charges', 0)
        disp = ad.get('disposition', '').replace('DISP_', '').replace('_', '+')
        if disp == 'UNDEFINED':
            disp = 'Byt'

        uri = ad.get('uri', '')
        link = f"https://www.bezrealitky.cz/nemovitosti-byty-domy/{uri}" if uri else ''
        tags = ad.get('tags({"locale":"CS"})', [])

        results.append({
            'disposition': disp,
            'surface': surface,
            'price': price,
            'charges': charges,
            'total': price + charges,
            'address': addr,
            'tags': tags,
            'url': link
        })

    return results[:limit]

def main():
    parser = argparse.ArgumentParser(description="Hledání bytů k pronájmu na Bezrealitky.cz")
    parser.add_argument('--location', type=str, default=None, help="Město nebo čtvrť (např. Praha, Ostrava, Brno)")
    parser.add_argument('--max-price', type=int, default=None, help="Maximální nájemné v Kč")
    parser.add_argument('--min-surface', type=int, default=None, help="Minimální plocha v m²")
    parser.add_argument('--limit', type=int, default=15, help="Počet zobrazených výsledků")
    parser.add_argument('--json', action='store_true', help="Výstup v JSON formátu")

    args = parser.parse_args()

    ads = fetch_bezrealitky_rentals(
        location=args.location,
        max_price=args.max_price,
        min_surface=args.min_surface,
        limit=args.limit
    )

    if args.json:
        print(json.dumps(ads, ensure_ascii=False, indent=2))
        return

    print(f"\n=== NALEZENÉ PRONÁJMY NA BEZREALITKY.CZ ({len(ads)}) ===")
    if not ads:
        print("Žádné nabídky neodpovídají zadaným kritériím.")
        return

    for i, a in enumerate(ads, 1):
        print(f"\n[{i}] {a['disposition']} ({a['surface']} m²) — {a['address']}")
        print(f"    Nájem: {a['price']:,} Kč | Poplatky: {a['charges']:,} Kč | Celkem: {a['total']:,} Kč/měs")
        if a['tags']:
            print(f"    Vlastnosti: {', '.join(a['tags'])}")
        print(f"    Odkaz: {a['url']}")

if __name__ == '__main__':
    main()
