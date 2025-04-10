import pandas as pd



# Converte para excel

df = pd.read_csv('produtos_amazonteste.csv')
df.to_excel('arquivo_convertido.xlsx', index=False, engine='openpyxl')
print("Conversão concluída!")