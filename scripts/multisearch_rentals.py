#!/usr/bin/env python3
"""
Unifikovaný vyhledávač pronájmů v ČR (Multisearch).
Agreguje data z prověřených a funkčních zdrojů:
1. Bezrealitky.cz (přímí majitelé, Apollo Cache)
2. Domonaut.cz (oficiální otevřené REST API s kaucemi)
3. Bazoš.cz (soukromá inzerce bez provize)
4. Sbazar.cz (inzerce Seznam API)
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3'
}

def search_bezrealitky(location=None, max_price=None, limit=10):
    results = []
    params = {'offerType': 'PRONAJEM', 'estateType': 'BYT', 'currency': 'CZK'}
    if max_price:
        params['priceTo'] = max_price
    url = f"https://www.bezrealitky.cz/vyhledat?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        next_data = soup.find('script', id='__NEXT_DATA__')
        if not next_data:
            return []
        cache = json.loads(next_data.string).get('props', {}).get('pageProps', {}).get('apolloCache', {})
        for ad in [v for k, v in cache.items() if k.startswith('Advert:')]:
            addr = ad.get('address({"locale":"CS"})') or ''
            foreign = ['Braniborsko', 'Sasko', 'Bayern', 'Hamburg', 'Nordrhein', 'Hessen', 'Mecklenburg', 'Baden', 'Bavorsko', 'Thüringen', 'Berlin', 'Bremen', 'Saarland', 'Porýní', 'Württembersko']
            if any(f.lower() in addr.lower() for f in foreign):
                continue
            price = ad.get('price', 0)
            if price < 4000:  # Vyřadí chybné importy v EUR
                continue
            if location and location.lower() not in addr.lower():
                continue
            price = ad.get('price', 0)
            if max_price and price > int(max_price):
                continue
            charges = ad.get('charges', 0)
            disp = ad.get('disposition', '').replace('DISP_', '').replace('_', '+')
            if disp == 'UNDEFINED': disp = 'Byt'
            surface = ad.get('surface', 0)
            uri = ad.get('uri', '')
            results.append({
                'source': 'Bezrealitky',
                'title': f"{disp} ({surface} m²)",
                'price': price,
                'charges': charges,
                'deposit': None,
                'address': addr,
                'url': f"https://www.bezrealitky.cz/nemovitosti-byty-domy/{uri}" if uri else ''
            })
            if len(results) >= limit:
                break
    except Exception as e:
        print(f"[Bezrealitky] Chyba: {e}", file=sys.stderr)
    return results

def search_domonaut(location=None, max_price=None, limit=10):
    results = []
    url = f"https://domonaut.cz/api/offers.php?limit={limit * 2}"
    dom_headers = {
        'User-Agent': 'VratmeDetiDomu-ApartmentFinder',
        'X-Domonaut-Agent': 'VratmeDetiDomu-ApartmentFinder',
        'X-Domonaut-Email': 'info@navratdetidomu.cz'
    }
    try:
        req = urllib.request.Request(url, headers=dom_headers)
        data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        for item in data.get('data', []):
            if item.get('typNabidky') != 'Pronájem':
                continue
            addr = f"{item.get('street', '')} {item.get('houseNumber', '')}, {item.get('level8', '')} {item.get('level6', '')}".strip(', ')
            if location and location.lower() not in addr.lower():
                continue
            price = item.get('cena', 0) or 0
            if max_price and price > int(max_price):
                continue
            results.append({
                'source': 'Domonaut API',
                'title': f"{item.get('disposition', 'Byt')} ({item.get('plocha', 0)} m²)",
                'price': price,
                'charges': item.get('poplatky', 0) or 0,
                'deposit': item.get('kauce'),
                'address': addr or 'Lokalita v inzerátu',
                'url': item.get('URL', '')
            })
            if len(results) >= limit:
                break
    except Exception as e:
        print(f"[Domonaut] Chyba: {e}", file=sys.stderr)
    return results

def search_bazos(location=None, max_price=None, limit=10):
    results = []
    query_parts = []
    if location:
        query_parts.append(location)
    q_str = urllib.parse.quote(' '.join(query_parts)) if query_parts else ''
    url = f"https://reality.bazos.cz/pronajmu/?hledat={q_str}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        for inz in soup.find_all('div', class_='inzeraty'):
            nadpis = inz.find('h2', class_='nadpis')
            cena_tag = inz.find('div', class_='inzeratycena')
            lokalita_tag = inz.find('div', class_='inzeratylokalita')
            if not nadpis:
                continue
            a_tag = nadpis.find('a')
            if not a_tag:
                continue
            title = nadpis.get_text(strip=True)
            price_raw = cena_tag.get_text(strip=True) if cena_tag else '0'
            price_digits = ''.join(c for c in price_raw if c.isdigit())
            price = int(price_digits) if price_digits else 0
            if max_price and price > int(max_price):
                continue
            addr = lokalita_tag.get_text(strip=True) if lokalita_tag else ''
            results.append({
                'source': 'Bazoš',
                'title': title,
                'price': price,
                'charges': 0,
                'deposit': None,
                'address': addr or (location or 'ČR'),
                'url': "https://reality.bazos.cz" + a_tag['href']
            })
            if len(results) >= limit:
                break
    except Exception as e:
        print(f"[Bazoš] Chyba: {e}", file=sys.stderr)
    return results

def main():
    parser = argparse.ArgumentParser(description="Multisearch nájemního bydlení v ČR (Bezrealitky, Domonaut, Bazoš)")
    parser.add_argument('--location', type=str, default=None, help="Lokalita (např. Praha, Ostrava, Brno)")
    parser.add_argument('--max-price', type=int, default=None, help="Maximální nájemné v Kč")
    parser.add_argument('--limit', type=int, default=15, help="Celkový limit výsledků")
    parser.add_argument('--json', action='store_true', help="Výstup v JSON")
    args = parser.parse_args()

    per_source = max(3, args.limit // 3)
    b_res = search_bezrealitky(location=args.location, max_price=args.max_price, limit=per_source)
    d_res = search_domonaut(location=args.location, max_price=args.max_price, limit=per_source)
    z_res = search_bazos(location=args.location, max_price=args.max_price, limit=per_source)

    all_res = b_res + d_res + z_res
    # Seřadit podle ceny vzestupně
    all_res.sort(key=lambda x: x['price'] if x['price'] > 0 else 999999)
    all_res = all_res[:args.limit]

    if args.json:
        print(json.dumps(all_res, ensure_ascii=False, indent=2))
        return

    print(f"\n=======================================================")
    print(f" MULTISEARCH REALITNÍCH NABÍDEK (Nalezeno: {len(all_res)})")
    if args.location:
        print(f" Lokalita: {args.location}")
    if args.max_price:
        print(f" Max cena: {args.max_price:,} Kč")
    print(f"=======================================================\n")

    if not all_res:
        print("Žádné nabídky neodpovídají zadaným kritériím.")
        return

    for i, item in enumerate(all_res, 1):
        dep_str = f" | Kauce: {item['deposit']:,} Kč" if item['deposit'] else ""
        chg_str = f" (+ {item['charges']:,} Kč popl.)" if item['charges'] else ""
        print(f"[{i}] [{item['source']}] {item['title']} — {item['price']:,} Kč{chg_str}{dep_str}")
        print(f"    Lokalita: {item['address']}")
        print(f"    Odkaz:    {item['url']}\n")

if __name__ == '__main__':
    main()
