import pandas as pd
import ast

# Carregando o arquivo CSV
df = pd.read_csv('produtos_amazon.csv')


def verficar_char_titulo(titulo):
    if len(titulo) > 200:
        return len(titulo), "Necessário alteração. Muito longo"
    elif len(titulo) < 30:
        return len(titulo), "Necessário alteração. Muito curto"
    
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
    
def verificar_video(video):
    if video == False:
        return "Adicionar um video"
    return "OK"

def verificar_fba(resultado):
    try:
        if resultado != "Amazon":
            return "Entrar para o FBA"
        return "OK"
    except Exception as e:
        return f"ERRO - {str(e)}"
    
def verificar_bullets(bullets):
    try:
        # Converte a string para lista real, removendo espaços extras e tratando erros
        lista = ast.literal_eval(bullets.strip())

        # Verifica se é de fato uma lista
        if not isinstance(lista, list):
            return "ERRO - Não é uma lista"

        qtd = len(lista)

        if qtd < 5:
            return f"Adicionar mais {5 - qtd} tópico(s)"
        return "OK"

    except Exception as e:
        return f"ERRO - {str(e)}"
