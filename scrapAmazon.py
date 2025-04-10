import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def iniciar_driver():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/123.0",
        "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
    ]

    user_agent = random.choice(user_agents)
    print(f"Usando user-agent: {user_agent}")

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--start-maximized')

    return webdriver.Chrome(options=options)

def coletar_elementos_produto(driver):
    return driver.find_elements(By.CSS_SELECTOR, 'div.s-result-item[data-asin][data-component-type="s-search-result"]')

def coletar_titulo(produto):
    try:
        return produto.find_element(By.CSS_SELECTOR, 'h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span').text
    except:
        return "Título não encontrado"

def rolar_pagina_suavemente(driver):
    altura_total = driver.execute_script("return document.body.scrollHeight")
    posicao = 0
    while posicao < altura_total:
        passo = random.randint(100, 300)
        posicao += passo
        driver.execute_script(f'window.scrollTo(0, {posicao});')
        time.sleep(random.uniform(0.2, 0.5))

def simular_mouse(driver):
    try:
        # Seleciona alguns elementos clicáveis ou que chamem atenção
        elementos = driver.find_elements(By.CSS_SELECTOR, 'a.a-link-normal')

        # Limita a quantidade para não exagerar
        elementos_visiveis = random.sample(elementos, min(3, len(elementos)))

        actions = ActionChains(driver)

        for el in elementos_visiveis:
            # Move o mouse até o elemento
            actions.move_to_element(el).pause(random.uniform(0.5, 1.5))

        actions.perform()

        # Adiciona pequenas pausas entre ações para parecer mais humano
        time.sleep(random.uniform(0.5, 1.2))

    except Exception as e:
        print(f"Erro na simulação de mouse: {e}")

def coletar_preco(produto):
    try:
        inteiro = produto.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
        centavos = produto.find_element(By.CSS_SELECTOR, 'span.a-price-fraction').text
        return f"R${inteiro},{centavos}"
    except:
        return "Preço não encontrado"

def coletar_avaliacao(driver):
    try:
        elemento_avaliacao = driver.find_element(By.CSS_SELECTOR, '[data-hook="rating-out-of-text"]')
        return elemento_avaliacao.text.strip()
    except Exception:
        return "Sem avaliação"

def ir_para_proxima_pagina(driver):
    try:
        botao_proxima = driver.find_element(By.CSS_SELECTOR, 'a.s-pagination-next')

        if 's-pagination-disabled' in botao_proxima.get_attribute('class'):
            return False
        
        # Scroll até o botão para garantir visibilidade
        driver.execute_script("arguments[0].scrollIntoView(true);", botao_proxima)
        time.sleep(1)  # pequeno delay para dar tempo de carregar

        # Força o clique via JavaScript
        driver.execute_script("arguments[0].click();", botao_proxima)

        # botao_proxima.click()
        return True
    except:    
        return False
    
def coletar_descricao(drive):
    try:
        paragrafos = driver.find_elements(By.CSS_SELECTOR, "#productDescription p")
        descricao = "\n".join(p.text.strip() for p in paragrafos if p.text.strip())
        return descricao if descricao else "Descrição vazia"
    except Exception as e:
        print(f"Erro ao coletar descrição: {e}")
        return "Descrição não encontrada"
    

def coletar_dados_produtos(driver):
    produtos_info = []

    while True:
        time.sleep(random.uniform(2, 5))
        rolar_pagina_suavemente(driver)
        simular_mouse(driver)
        time.sleep(random.uniform(1, 3))

        produtos = coletar_elementos_produto(driver)

        for produto in produtos:
            titulo = coletar_titulo(produto)
            preco = coletar_preco(produto)

            # Coleta o link do produto
            link = produto.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-no-outline').get_attribute("href")

            # Abre nova aba com o link
            driver.execute_script(f"window.open('{link}');")
            driver.switch_to.window(driver.window_handles[1])
            rolar_pagina_suavemente(driver)
            time.sleep(random.uniform(2, 4))

            # Coleta dados da página individual
            descricao = coletar_descricao(driver)
            avaliacao = coletar_avaliacao(driver)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.uniform(1.5, 3.5))

            if titulo != "Título não encontrado" and preco != "Preço não encontrado":
                produtos_info.append({
                    "titulo": titulo,
                    "preco": preco,
                    "descricao": descricao,
                    "avaliacao": avaliacao
                })

        if not ir_para_proxima_pagina(driver):
            break

    return produtos_info

def salvar_produtos_em_csv(lista_de_produtos, nome_arquivo="produtos_amazonteste.csv"):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        campos = ["titulo", "preco", "descricao", "avaliacao"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for produto in lista_de_produtos:
            escritor.writerow(produto)

# ----------- EXEMPLO DE USO -----------
if __name__ == "__main__":
    driver = iniciar_driver()
    driver.get("https://www.amazon.com.br/s?i=merchant-items&me=A2ZYQFB9FA7MU3&marketplaceID=A2Q3Y263D00KWC&qid=1744132770&xpid=tqkuqdh5H_SQg&ref=sr_pg_1")

    time.sleep(3)  # Espera inicial

    produtos = coletar_dados_produtos(driver)
    salvar_produtos_em_csv(produtos)

    driver.quit()
    print("Produtos salvos com sucesso.")
