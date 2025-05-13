import pandas as pd
import ast


# Carregando o arquivo CSV
df = pd.read_csv('produtos_amazonteste.csv')

def verficar_char_titulo(titulo):
    if len(titulo) > 200:
        return len(titulo), "Necessário alteração. Muito longo"
    return len(titulo), "OK"

def verificar_qualidade_imagem(resolucao):
    try:
        largura, altura = map(int, resolucao.lower().split('x')) # lower transforma todos o char em minusculas
                                                                 # split transforma a string em uma lista e diz que o separador da string será um 'x' "1200x800".split('x') → ["1200", "800"]
        if largura > 1100 and altura > 1100:
            return resolucao, "OK"
        elif (largura >= 1000 or altura >=1000) and (altura <=1100 or largura <= 1100):
            return resolucao, "OK" 
        return resolucao, "Necessário alteração. Baixa resolução"
    except Exception as e:
        return resolucao, f"ERRO - {str(e)}"
    
def verificar_quantidade_imagens(imagens):
    try:
        qtd = int(imagens)
        if qtd < 6:
            return f'Adicionar mais {6 -qtd} imagens'
        return "OK"
    except Exception as e:
        return f"ERRO - {str(e)}"

def verificar_video(video):
    if video == False:
        return "Adicionar um video"
    return "OK"

def verificar_fba(resultado):
    try:
        if resultado != "Amazon":
            return "Entrar para o FBA"
        return "Sim"
    except Exception as e:
        return f"ERRO - {str(e)}"

def verificar_categoria(resultado):
    try:
        if resultado != "Categoria não encontrada":
            return resultado
    except Exception as e:
        return f"ERRO - {str(e)}"
    
def verificar_ranking(ranking):
    try:
        if ranking != "Indisponível":
            return ranking
        return "null"
        
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

def verificar_avaliacao(avaliacao):
    try:
        # Verifica se a avaliação é 'Sem avaliação'
        if avaliacao == 'Sem avaliação':
            return 'null'
        
        # Caso contrário, tenta extrair o valor da avaliação
        nota = float(avaliacao.split(' de ')[0].replace(',', '.'))  # Converte a nota para float
        
        # Classificação da avaliação
        if nota >= 4.5:
            return f"OK - {nota}, Ótima"
        elif nota < 4.5 and nota >= 4.2:
            return f"OK - {nota}, Boa"
        elif nota >= 3.9 and nota < 4.2:
            return f"Incentivar + review positivo - {nota}"
        else:
            return f"Incentivar + review positivo - {nota}"
    
    except Exception as e:
        return f"ERRO - {str(e)}"

def verificar_preco(preco):
    try:
        if preco != "Indisponível":
            return preco
        return "-"
    except Exception as e:
        return f"ERRO - {str(e)}"

def calcular_relevancia(nota, qtd_avalicao):
    peso_qtd_avaliacao = 0.6  # Importância das avaliações no ranking
    peso_media_nota = 0.4     # Importância da nota média

    # Tratar a avaliação (transforma '4,3 de 5' em 4.3 e 'Sem avaliação' em 0.0)
    if nota == "Sem avaliação":
        nota_tratada = 0.0
    else:
        try:
            # Tenta converter a nota para float, caso contrário, atribui 0
            nota_tratada = float(nota.split(" de")[0].replace(',', '.'))
        except Exception as e:
            print(f"Erro ao tratar avaliação: {nota} → {e}")
            nota_tratada = 0.0

    # Tratar a quantidade de avaliações (remover pontos e transformar em inteiro)
    try:
        # Verificar se qtd_avalicao é uma string com números
        qtd_aval_tratada = int(str(qtd_avalicao).replace('.', '').strip())
    except Exception as e:
        print(f"Erro ao tratar qtd_avaliacao: {qtd_avalicao} → {e}")
        qtd_aval_tratada = 0

    # Se não houver avaliações, retorna relevância 0
    if qtd_aval_tratada == 0:
        return 0
    
    # Calcula a relevância com base nos pesos
    relevancia = (qtd_aval_tratada * peso_qtd_avaliacao) + (nota_tratada * 20 * peso_media_nota)
    relevancia = min(relevancia, 100)  # Garante que a relevância não ultrapasse 100
    
    return round(relevancia, 2)

def verificar_qtd_avaliacao(qtd_avaliacao):
    try:
        if qtd_avaliacao == 0:
            return '-'
        return qtd_avaliacao
    except Exception as e:
        return f"ERRO - {str(e)}"


df_result = pd.DataFrame({
    'Titulo': df['titulo'],
    'Título_Verif': df['titulo'].apply(verficar_char_titulo),
    'Categoria': df['nome_categoria'].apply(verificar_categoria),
    'Link': df['link'],
    'Ranking': df['ranking'].apply(verificar_ranking),
    'Avaliação': df['avaliacao'].apply(verificar_avaliacao),
    'Qtd_Avaliação': df['qtd_avaliacao'].apply(verificar_qtd_avaliacao),
    'Relevância': df.apply(lambda row: calcular_relevancia(row['avaliacao'], row['qtd_avaliacao']),axis=1),
    'Qualidade da Imagem': df['qualidade_imagem'].apply(verificar_qualidade_imagem),
    'Quantidade de Imagens': df['qtd_imagem'].apply(verificar_quantidade_imagens),
    'Vídeos': df['video'].apply(verificar_video),
    'FBA': df['fba'].apply(verificar_fba),
    'Bullets': df['bullets'].apply(verificar_bullets),
    'Data': df['data_coleta']
})

df_result.to_csv('erros.csv', index=False)  # Salva em CSV
df_result.to_excel('erros.xlsx', index=False)  # Salva em XLSX

print("Arquivos salvos com sucesso!")

