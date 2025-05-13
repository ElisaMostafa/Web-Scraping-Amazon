import pandas as pd



# Converte para excel

df = pd.read_csv('produtos_amazon.csv')
df.to_excel('produtos_amazon.xlsx', index=False, engine='openpyxl')
print("Conversão concluída!")