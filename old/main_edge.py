from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
from siop_utils import preencher_input_por_id, preenche_seletor_por_id, clicar_botao
from siop_utils import preenche_seletor_por_xpath, preencher_input_por_xpath
from siop_utils import get_elemento, get_url

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
    caminho = os.path.expandvars(r'%LOCALAPPDATA%\\Microsoft\\Edge\\User Data')
    caminho_ajustado = re.sub(r'\\+', r'\\\\', caminho) 
    argumento = f'--user-data-dir={caminho_ajustado}'
    edge_options.add_argument(argumento)
    edge_options.add_argument('--profile-directory=Default')
    return webdriver.Edge(options=edge_options)

def seleciona_ano_e_perfil(driver, wait, ano, perfil):
    preenche_seletor_por_xpath(driver, wait, "Exercício", '//label[contains(text(), "Exercício")]/following-sibling::div/select', ano)
    preenche_seletor_por_xpath(driver, wait, "Perfil", '//label[contains(text(), "Perfil")]/following-sibling::div/select', perfil)


def listar_objetivo_específico(driver, wait, objetivo, ano, perfil):  
    driver.get(get_url("listar_objetivo_específico"))
    seleciona_ano_e_perfil(driver, wait, ano, perfil)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
    print("✅ Container principal carregado.")
    preencher_input_por_xpath(driver, wait, "Objetivo Específico",
        get_elemento("ppa.objetivo_especifico.objetivo_especifico_input", "xpath"), objetivo
    )    
    clicar_botao(driver, wait, texto="Procurar")    

def listar_programa(driver, wait, programa, ano, perfil):  
    driver.get(get_url("listar_programa"))
    seleciona_ano_e_perfil(driver, wait, ano, perfil)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
    print("✅ Container principal carregado.")
    preencher_input_por_xpath(driver, wait, "Programa",
        get_elemento("ppa.programa.programa_input", "xpath"), programa
    )    
    clicar_botao(driver, wait, texto="Procurar")    

def main():
    driver = iniciar_driver()
    wait = WebDriverWait(driver, 120)   
      
    #listar_objetivo_específico(driver, wait, "0002", "2025", "Controle de Qualidade - SEPLAN")
    listar_programa(driver, wait, "1144", "2025", "Controle de Qualidade - SEPLAN")

    time.sleep(20)
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
