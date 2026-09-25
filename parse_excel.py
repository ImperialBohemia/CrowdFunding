import pandas as pd

file_path = '/home/q/Downloads/weby-os-02-2026.xlsx'
df = pd.read_excel(file_path)

# Let's just print the columns and the first 10 rows to see the structure
print("Columns:", df.columns.tolist())
print(df.head(10).to_string())
