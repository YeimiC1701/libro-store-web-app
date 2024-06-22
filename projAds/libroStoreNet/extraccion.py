import pandas as pd

# def extraer_datos():
df = pd.read_csv('CPdescarga.txt', sep = '|', encoding = 'latin-1')
df = df[['d_codigo', 'd_asenta', 'D_mnpio', 'd_estado', 'id_asenta_cpcons']]
print(df.head())
