from scrapAmazon import iniciar_driver, coletar_bullet_points, rolar_pagina_suavemente, simular_mouse, coletar_imagem, coletar_qualidade_imagem, coletar_qtd_imagem
import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL de teste individual
URL_TESTE = "https://www.amazon.com.br/Biqu%C3%ADni-Avia%C3%A7%C3%A3o-Estampado-Conforto-Estilo/dp/B0DKQY7HWC/ref=sr_1_4?dib=eyJ2IjoiMSJ9.4YYKbH1FfKIA9rxCyn6qBqKyVedKZ51ysFeKmZAIvmyYiBZ6Yra0VaWpB3XK0NGJQlHlPDvCTs4xj1aJdNQ_BR8AYpPwrFZE2OTNolapTE6_iczqLloCzkphVahTzx3veDL2z_HkfGPnuHAELnO5vtQHM2C6GfYJGfyv6QSm2BXmbq7c5vSwFYWP-1BsUHCTFt0IM688CsCW_i16kQCccezCleGMJe6Ktj8SfIRJzE8.yDnp-HIGEXP9y77yD83dCOqAUwbLMXHesdWCHVn3fu0&dib_tag=se&m=A2ZYQFB9FA7MU3&marketplaceID=A2Q3Y263D00KWC&qid=1744383651&s=merchant-items&sr=1-4&ufe=app_do%3Aamzn1.fos.6d798eae-cadf-45de-946a-f477d47705b9&xpid=tqkuqdh5H_SQg"  # link de produto desejado

def teste():
    driver = iniciar_driver()
    try:
        driver.get(URL_TESTE)

        # Espera inicial com comportamento humano
        time.sleep(random.uniform(2.5, 4.5))
        
        simular_mouse(driver)
        time.sleep(random.uniform(1.5, 3.5))

        imagens = coletar_imagem(driver) 
        quantidade = coletar_qtd_imagem(driver)
        qualidade_imagem = coletar_qualidade_imagem(driver)# >>>>> FUNÇÃO A SER TESTADA
        
        print(qualidade_imagem)

        # for imagem in imagens:
        #     print(f"- {imagem}")

    except Exception as e:
        print("Erro no teste:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    teste()
