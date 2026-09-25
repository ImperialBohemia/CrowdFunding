import pandas as pd

file_path = '/home/q/Downloads/weby-os-02-2026.xlsx'
df = pd.read_excel(file_path)

for index, row in df.iterrows():
    domain = str(row.get('Doména', '')).lower()
    if 'mim' in domain or 'zena' in domain or 'matk' in domain or 'rodin' in domain:
        print(domain)
