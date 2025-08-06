from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
#from siop_utils import preencher_input_por_id, preenche_seletor_por_id
from siop_utils import clicar_botao
from siop_utils import preenche_seletor_por_xpath, preencher_input_por_xpath
from siop_utils import get_elemento, get_url
import siop_utils

import os
import re
import json


def finaliza_navegador():
# Finaliza instâncias anteriores do Edge
    try:
        subprocess.run([
            "powershell", "-Command",
            "Stop-Process -Name 'msedge' -Force -ErrorAction SilentlyContinue"
        ], check=True)
        print("🧹 Edge encerrado com sucesso antes da execução.")
    except subprocess.CalledProcessError:
        print("⚠️ Não foi possível encerrar processos do Edge ou nenhum processo estava ativo.")


def iniciar_driver():
    edge_options = Options()
    edge_driver_path = r"C:\SEPLAN\selenium_siop-main\drivers\edge\msedgedriver.exe"
    service = Service(executable_path=edge_driver_path)
    options = Options()
    caminho = os.path.expandvars(r'%LOCALAPPDATA%\\Microsoft\\Edge\\User Data')
    caminho_ajustado = re.sub(r'\\+', r'\\\\', caminho) 
    argumento = f'--user-data-dir={caminho_ajustado}'
    edge_options.add_argument(argumento)
    edge_options.add_argument('--profile-directory=Default')
    return webdriver.Edge(service=service, options=edge_options)

def seleciona_ano_e_perfil(ano, perfil):
    print(get_elemento("exercicio", "xpath"))
    preenche_seletor_por_xpath("Exercício", get_elemento("exercicio", "xpath"), ano) #'//label[contains(text(), "Exercício")]/following-sibling::div/select'
    preenche_seletor_por_xpath("Perfil", get_elemento("perfil", "xpath"), perfil) #'//label[contains(text(), "Perfil")]/following-sibling::div/select'


def listar_objetivo_específico(objetivo, ano, perfil):  
    driver.get(get_url("listar_objetivo_específico"))
    seleciona_ano_e_perfil(ano, perfil)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
    print("✅ Container principal carregado.")
    preencher_input_por_xpath("Objetivo Específico",
        get_elemento("ppa.objetivo_especifico.objetivo_especifico_input", "xpath"), objetivo
    )    
    clicar_botao(texto="Procurar")    

def listar_programa(programa, ano, perfil):  
    driver.get(get_url("listar_programa"))
    seleciona_ano_e_perfil(ano, perfil)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
    print("✅ Container principal carregado.")
    preencher_input_por_xpath("Programa", get_elemento("ppa.programa.programa_input", "xpath"), programa)    
    clicar_botao(texto="Procurar")    

def main():
    global driver, wait
    driver = iniciar_driver()
    wait = WebDriverWait(driver, 120)   
    siop_utils.driver = driver
    siop_utils.wait = wait

    ano = "2025"
    perfil = "Controle de Qualidade - SEPLAN"
      
    listar_objetivo_específico("0002", ano, perfil)
    time.sleep(5)
    listar_programa("1144", ano, perfil)

    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    print ("iniciando")

    #resposta = input("\n⚠️ Você precisa estar previamente logado no SIOP.\n\nO navegador Microsoft Edge será fechado. Deseja continuar? (s/n): ").strip().lower()

    #if resposta != 's':
    #    print("Operação cancelada pelo usuário.")
    #    sys.exit(0)
    finaliza_navegador()
    main()
    
    #print(get_elemento("ppa.programa.programa_input", "xpath"))
    #print(get_url("listar_objetivo_específico"))
