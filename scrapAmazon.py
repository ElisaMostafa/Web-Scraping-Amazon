import time
import csv
import random
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
from io import BytesIO
import requests
import os

def iniciar_driver():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.129 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.91 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6415.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6460.70 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Chrome/124.0.6367.78 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Chrome/135.0.7049.85 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; rv:134.0) Gecko/20100101 Chrome/134.0.6997.54 Safari/537.36"
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
    
def coletar_data_extracao():
    return datetime.now().strftime("%d/%m/%Y")

def coletar_avaliacao(driver):
    try:
        elemento_avaliacao = driver.find_element(By.CSS_SELECTOR, '[data-hook="rating-out-of-text"]')
        return elemento_avaliacao.text.strip()
    except Exception:
        return "Sem avaliação"

def coletar_quantidade_avaliacoes(driver):
    try:
        elemento = driver.find_element(By.ID, 'acrCustomerReviewText')
        texto = elemento.text  # Exemplo: "31 avaliações de clientes"
        numero = int(''.join(filter(str.isdigit, texto)))
        return numero
    except Exception as e:
        print(f"Erro ao coletar avaliações: {e}")
        return 0

def coletar_bullet_points(driver):
    try:
        # Primeira tentativa: bullets no bloco com spacing-small
        elementos = driver.find_elements(By.CSS_SELECTOR, 'ul.a-unordered-list.a-vertical.a-spacing-small li span.a-list-item')
        bullets = [el.text.strip() for el in elementos if el.text.strip()]

        # Se não encontrou nada, tenta no bloco com spacing-mini
        if not bullets:
            elementos = driver.find_elements(By.CSS_SELECTOR, 'ul.a-unordered-list.a-vertical.a-spacing-mini li span.a-list-item')
            bullets = [el.text.strip() for el in elementos if el.text.strip()]

        return bullets if bullets else ["Bullet points não encontrados"]

    except Exception as e:
        print(f"Erro ao coletar bullet points: {e}")
        return ["Erro ao coletar bullet points"]

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
    
def coletar_descricao(driver):
    try:
        paragrafos = driver.find_elements(By.CSS_SELECTOR, "#productDescription p")
        descricao = "\n".join(p.text.strip() for p in paragrafos if p.text.strip())
        return descricao if descricao else "Descrição vazia"
    except Exception as e:
        print(f"Erro ao coletar descrição: {e}")
        return "Descrição não encontrada"

def coletar_imagem(driver):
    try:  
        imagem_elemento = driver.find_element(By.CSS_SELECTOR, "div.imgTagWrapper img")
        imagem_alta = imagem_elemento.get_attribute("data-old-hires")
        if imagem_alta:
            return imagem_alta
        else:
            return imagem_elemento.get_attribute("src")  # fallback se o data-old-hires estiver vazio
    except Exception as e:
        print(f"[ERRO] coletar_imagem: {type(e).__name__} - {str(e)}")
        return None

def coletar_qtd_imagem(driver):
    try:
        miniaturas = driver.find_elements(By.CSS_SELECTOR, "li.imageThumbnail img")
        miniaturas_visiveis = [m for m in miniaturas if m.is_displayed()]
        return len(miniaturas_visiveis)
    except Exception as e:
        print(f"Erro ao coletar miniaturas: {e}")
        return 0

def verificar_video(driver):
    try:
        video_elementos = driver.find_elements(By.CSS_SELECTOR, "li.videoThumbnail video")
        for v in video_elementos:
            if v.is_displayed():
                return True
        return False
    except Exception as e:
        print(f"Erro ao verificar vídeo: {e}")
        return False
    
def coletar_qualidade_imagem(driver):
    try:
        img_principal = driver.find_element(By.CSS_SELECTOR, "img.a-dynamic-image")
        img_url = img_principal.get_attribute("data-old-hires")

        if not img_url:
            print("[ERRO] Atributo data-old-hires não encontrado.")
            return None

        # Faz o download da imagem
        response = requests.get(img_url)
        image = Image.open(BytesIO(response.content))

        largura, altura = image.size
        return f"{largura}x{altura}"

    except Exception as e:
        print(f"[ERRO] qualidade_imagem: {e}")
        return None

def coletar_categoria(driver):
    try:
        # Encontrar o último item da lista de categorias (geralmente o mais específico)
        categoria_elementos = driver.find_elements(By.CSS_SELECTOR, "li span.a-list-item a.a-link-normal.a-color-tertiary")
        
        if categoria_elementos:
            categoria = categoria_elementos[-1]  # A mais específica costuma ser a última
            nome_categoria = categoria.text.strip()
            link_categoria = categoria.get_attribute("href")
            return nome_categoria, link_categoria
        else:
            return "Categoria não encontrada", "Link não encontrado"
        
    except Exception as e:
        print(f"Erro ao coletar categoria: {e}")
        return "Categoria não encontrada", "Link não encontrado"

def coletar_fba(driver):
    try: 
        fba_elemento = driver.find_element(By.CSS_SELECTOR, "div span.a-size-small.offer-display-feature-text-message")
        return fba_elemento.text.strip()
    except Exception as e:
        print(f"Erro ao coletar FBA: {e}")
        return "FBA não encontrado"

def coletar_ranking(driver): 
    try:
        elemento_td = driver.find_element(
            By.XPATH,
            '//th[contains(text(), "Ranking dos mais vendidos")]/following-sibling::td'
        )
        texto_ranking = elemento_td.text.strip()

        # Pegar todos os rankings com ponto ou sem ponto (ex: 66.558 ou 863)
        matches = re.findall(r'N[ºo]?\s*([\d\.]+)', texto_ranking)

        if matches:
            # Pegar o ÚLTIMO ranking da lista (o mais específico, ex: Hubs USB)
            ranking_texto = matches[-1].replace('.', '')  # remover o ponto dos milhares
            return int(ranking_texto)
        else:
            print("Ranking não encontrado no texto:", texto_ranking)
            return None

    except NoSuchElementException:
        print("Elemento de ranking não encontrado.")
        return "Indisponível"
    
def coletar_nome_vendedor(driver):
    try:
        nome_elemento = driver.find_element(By.ID, "sellerProfileTriggerId")
        nome_bruto = nome_elemento.text.strip()
        nome_formatado = nome_bruto.replace(" ", "").replace(".", "").replace(",", "").replace("-", "").replace("/", "")
        return nome_formatado
    except Exception as e:
        print(f"Erro ao coletar nome do vendedor: {e}")
        return "Nome não encontrado"

def coletar_dados_produtos(driver):
    produtos_info = []

    while True:
        time.sleep(random.uniform(2, 6))
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
            qtd_avaliacao = coletar_quantidade_avaliacoes(driver)
            bullets = coletar_bullet_points(driver)
            imagem = coletar_imagem(driver)
            qtd_imagem = coletar_qtd_imagem(driver)
            qualidade_imagem = coletar_qualidade_imagem(driver)
            video = verificar_video(driver)
            nome_categoria, link_categoria = coletar_categoria(driver)
            ranking = coletar_ranking(driver)
            fba = coletar_fba(driver)
            
            
            

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.uniform(1.5, 3.5))

            if titulo != "Título não encontrado" and preco != "Preço não encontrado":
                produtos_info.append({
                    "titulo": titulo,
                    "preco": preco,
                    "link": link,
                    "descricao": descricao,
                    "avaliacao": avaliacao,
                    "qtd_avaliacao": qtd_avaliacao,
                    "bullets": bullets,
                    "imagem": imagem,
                    "qtd_imagem": qtd_imagem,
                    "qualidade_imagem": qualidade_imagem,
                    "video": video,
                    "nome_categoria": nome_categoria,
                    "ranking": ranking,
                    "link_categoria": link_categoria,
                    "fba": fba,
                    "data_coleta": datetime.now().strftime("%d/%m/%Y")
                    
                })

        if not ir_para_proxima_pagina(driver):
            break

    return produtos_info

def salvar_produtos_em_csv(lista_de_produtos, nome_arquivo=f"produtos_amazonteste.csv"):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        campos = ["titulo", "preco", "link", "descricao", "avaliacao", "qtd_avaliacao", "bullets", "imagem", "qtd_imagem", "qualidade_imagem", "video", "nome_categoria", "ranking", "link_categoria", "fba", "data_coleta"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for produto in lista_de_produtos:
            escritor.writerow(produto)


# ------------------------------------------ EXECUÇÃO PRINCIPAL --------------------------------------------------
if __name__ == "__main__":
    driver = iniciar_driver()
    driver.get("https://www.amazon.com.br/s?i=merchant-items&me=A2ZYQFB9FA7MU3&marketplaceID=A2Q3Y263D00KWC&qid=1744132770&xpid=tqkuqdh5H_SQg&ref=sr_pg_1")

    time.sleep(3)  # Espera inicial

    produtos = coletar_dados_produtos(driver)
    salvar_produtos_em_csv(produtos)

    driver.quit() 
    print("Produtos salvos com sucesso.")


