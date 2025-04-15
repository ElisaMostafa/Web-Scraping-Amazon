import pandas as pd

# Carregando o arquivo CSV
df = pd.read_csv('produtos_amazonteste.csv')

def verficar_char_titulo(titulo):
    if len(titulo) > 200:
        return len(titulo), "ERRADO - Acima de 200"
    return len(titulo), "OK"

def verificar_qualidade_imagem(resolucao):
    try:
        largura, altura = map(int, resolucao.lower().split('x')) # lower transforma todos o char em minusculas
                                                                 # split transforma a string em uma lista e diz que o separador da string será um 'x' "1200x800".split('x') → ["1200", "800"]
        if largura > 1100 and altura > 1100:
            return resolucao, "OK"
        elif (largura >= 1000 or altura >=1000) and (altura <=1100 or largura <= 1100):
            return resolucao, "Media" 
        return resolucao, "Ruim"
    except Exception as e:
        return resolucao, f"ERRO - {str(e)}"
    
def verificar_quantidade_imagens(imagens):
    qtd = int(imagens)
    if qtd < 6:
        return f'Adicionar mais {6-qtd} imagens'
    return "OK"

def verificar_video(video):
    if video == False:
        return "Adicionar um video"
    return "OK"


df_result = pd.DataFrame({
    'Título': df['titulo'].apply(verficar_char_titulo),
    'Qualidade da Imagem': df['qualidade_imagem'].apply(verificar_qualidade_imagem),
    'Quantidade de Imagens': df['qtd_imagem'].apply(verificar_quantidade_imagens),
    'Vídeos': df['video'].apply(verificar_video)
})

print(df['video'])

print(df_result)



