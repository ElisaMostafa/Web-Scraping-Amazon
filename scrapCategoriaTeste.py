import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from scrapAmazon import coletar_titulo, coletar_preco, coletar_avaliacao  # Adicione aqui outras funções que precisar

# Caminho para o arquivo base
ARQUIVO_BASE = 'produtos_amazonteste.csv'

# Pasta onde os arquivos serão salvos
PASTA_SAIDA = 'concorrentes'
os.makedirs(PASTA_SAIDA, exist_ok=True)

# Configuração do driver
def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f"user-agent={gerar_user_agent()}")
    driver = webdriver.Chrome(options=options)
    return driver

# Geração de user-agent aleatório
def gerar_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    ]
    return random.choice(user_agents)

# Rolagem suave
def rolar_pagina(driver):
    for _ in range(random.randint(3, 6)):
        driver.execute_script("window.scrollBy(0, window.innerHeight/2);")
        time.sleep(random.uniform(0.8, 1.6))

# Verifica nome de arquivo sem sobrescrever
def nome_arquivo_categoria(categoria, usados):
    base = categoria.strip().replace("/", "_")
    nome = base
    contador = 1
    while nome in usados:
        nome = f"{base}_{contador}"
        contador += 1
    usados.add(nome)
    return nome

## >> modificar aqui, pois o programa esta acessando cada link_categoria e pesquisando na barra de pesquisa (adicionar código para a pesquisar ser mais humanizada, digitando caracter por caracter), mas encontra algum erro ao salvar as informações corretamente. Verifiquei que o programa está fazendo tudo muito rápido, então o erro pode ser porque não teve tempo de carregar a página por completo ainda (adicionar sleep e waitdriver).

# Busca concorrentes de um produto
def buscar_concorrentes(driver, categoria, link_categoria, titulo_busca):
    driver.get(link_categoria)
    time.sleep(random.uniform(2, 4))
    rolar_pagina(driver)

    # Pesquisa na barra de busca >>>>>>>> MODIFICAR AQUI (digitando mt rapdio) <<<<<<<<<<
    try:
        barra = driver.find_element(By.ID, 'twotabsearchtextbox')
        barra.clear()
        barra.send_keys(titulo_busca)
        barra.send_keys(Keys.RETURN)
        time.sleep(random.uniform(2, 4))
    except Exception as e:
        print(f"Erro ao pesquisar produto: {e}")
        return []

    rolar_pagina(driver)

    produtos = []
    resultados = driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div[data-asin]')[:10] 
    for i, produto in enumerate(resultados):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", produto)
            link = produto.find_element(By.CSS_SELECTOR, 'h2 a').get_attribute('href')
            driver.execute_script("window.open(arguments[0]);", link)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(random.uniform(2, 4))

            # >>>>>>>>>>>>>>>>> ADICIONAR MAIS CAMPOS (trazer todos os campos)<<<<<<<<<<<<<<<<<<
            titulo = coletar_titulo(driver)
            preco = coletar_preco(driver)
            avaliacao = coletar_avaliacao(driver)

            produtos.append({
                'Título': titulo,
                'Preço': preco,
                'Avaliação': avaliacao,
                'Link': driver.current_url
            })

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Erro no produto {i+1}: {e}")
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            continue

    return produtos

# Processo principal
def main():
    df = pd.read_csv(ARQUIVO_BASE)
    usados = set()

    driver = iniciar_driver()

    for index, row in df.iterrows():
        categoria = str(row['nome_categoria']).strip()
        link_categoria = row['link_categoria']
        titulo_produto = str(row['titulo']).strip()

        print(f"\n🟡 Coletando concorrentes para: {titulo_produto} | Categoria: {categoria}")
        dados = buscar_concorrentes(driver, categoria, link_categoria, titulo_produto)

        if dados:
            nome = nome_arquivo_categoria(categoria, usados)
            caminho = os.path.join(PASTA_SAIDA, f"{nome}.csv")
            pd.DataFrame(dados).to_csv(caminho, index=False)
            print(f"✅ Salvo: {caminho}")
        else:
            print(f"⚠️ Nenhum concorrente coletado para: {titulo_produto}")

    driver.quit()
    print("\n✅ Finalizado!")

if __name__ == "__main__":
    main()
