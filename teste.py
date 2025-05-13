from scrapAmazon import (iniciar_driver, coletar_ranking, simular_mouse)
import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# URL de teste individual
URL_TESTE = "https://www.amazon.com.br/Pel%C3%ADcula-Protetora-Motorola-Celular-Transparente/dp/B075DZL4X6/ref=sr_1_11?dib=eyJ2IjoiMSJ9.an_1cY7E3LZNeVFRP4TQyz7_H4IYPNFkgGxEwby91AkKywokTOlb8c8SKWTmidMQySxXYjgIW_zxf9-tjXk7MPMZVY30GMRz8mmI4G4KkkrrgzByzMWpF5NtUA4A1GbvGj2xXOvznxaPCE_j3Fhst02QylxaUedF9OxRXxxUodmWq1v7F0_mvfeKst6WIkqLQAt0furxmrQjl4I1KCGhVsmIlF2fwcRAlVDBdXWXph0.wQlh-o4QK9z9yJUm6GccLO5AkkoaYbNpDCV6f1hifJ0&dib_tag=se&m=A2ZYQFB9FA7MU3&marketplaceID=A2Q3Y263D00KWC&qid=1744888259&s=merchant-items&sr=1-11&xpid=tqkuqdh5H_SQg"  # link de produto desejado

def teste():
    driver = iniciar_driver()
    try:
        driver.get(URL_TESTE)

        # Espera inicial com comportamento humano
        time.sleep(random.uniform(2.5, 4.5))
        
        simular_mouse(driver)
        time.sleep(random.uniform(1.5, 3.5))

        resultado = coletar_ranking(driver)
        print(f'Ranking: {resultado}')# >>>>> FUNÇÃO A SER TESTADA
        

        
        
        # for imagem in imagens:
        #     print(f"- {imagem}")
        

    except Exception as e:
        print("Erro no teste:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    teste()
    
