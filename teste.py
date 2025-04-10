import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


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

def rolar_pagina_suavemente(driver):
    altura_total = driver.execute_script("return document.body.scrollHeight")
    posicao = 0
    while posicao < altura_total:
        passo = random.randint(100, 300)
        posicao += passo
        driver.execute_script(f"window.scrollTo(0, {posicao});")
        time.sleep(random.uniform(0.2, 0.5))

def coletar_elementos_produto(driver):
    return driver.find_elements(By.CSS_SELECTOR, 'div.s-result-item[data-asin][data-component-type="s-search-result"]')

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
    
if __name__ == "__main__":
    driver = iniciar_driver()
    driver.get("https://www.amazon.com.br/s?i=merchant-items&me=A2ZYQFB9FA7MU3&marketplaceID=A2Q3Y263D00KWC&qid=1744132770&xpid=tqkuqdh5H_SQg&ref=sr_pg_1")

    time.sleep(3)  # Espera inicial

    rolar_pagina_suavemente(driver)
    coletar_elementos_produto(driver)
    ir_para_proxima_pagina(driver)

    driver.quit()
    print("Produtos salvos com sucesso.")