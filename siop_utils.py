from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import subprocess

import time
import json
import os
import pandas as pd
from config import config
import re


driver = None
wait = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def iniciar_driver():
    global driver, wait

    edge_options = Options()
    edge_driver_path = config.DRIVER_DIR
    print(f"Driver edge: {edge_driver_path}")
    service = Service(
        executable_path=config.DRIVER_DIR,
        log_path="logs/edge_driver.log",  # opcional
        service_args=["--verbose"],
        creationflags=subprocess.CREATE_NO_WINDOW  # oculta janela do EdgeDriver
    )

    caminho = os.path.expandvars(config.EDGE_DIR)
    caminho_ajustado = re.sub(r'\\+', r'\\\\', caminho)
    argumento = f'--user-data-dir={caminho_ajustado}'
    edge_options.add_argument(argumento)
    edge_options.add_argument('--profile-directory=Default')

    driver = webdriver.Edge(service=service, options=edge_options)
    return driver

# Carrega os elementos do JSON uma vez
with open(os.path.join(BASE_DIR, "config/elementos.json"), "r", encoding="utf-8") as f:
    _elementos = json.load(f)

with open(os.path.join(BASE_DIR, "config/urls.json"), "r", encoding="utf-8") as f:
    _urls = json.load(f)

def get_elemento_(nome_item, tipo):
    for elem in _elementos:
        if elem["item"] == nome_item:
            return elem.get(tipo)
    raise ValueError(f"Elemento '{nome_item}' com tipo '{tipo}' não encontrado.")

def get_elemento_xpath(nome_item):
    tipo = "xpath"
    for elem in _elementos:
        if elem["item"] == nome_item:
            return elem.get(tipo)
    raise ValueError(f"Elemento '{nome_item}' com tipo '{tipo}' não encontrado.")

def get_elemento_id(nome_item):
    tipo = "id"
    for elem in _elementos:
        if elem["item"] == nome_item:
            return elem.get(tipo)
    raise ValueError(f"Elemento '{nome_item}' com tipo '{tipo}' não encontrado.")

def get_url(atividade):
    for item in _urls:
        if item["atividade"] == atividade:
            return item["url"]
    raise ValueError(f"URL para atividade '{atividade}' não encontrada.")

def acessa_url(url):
    driver.get(config.URL_BASE + url)

def abrir_excel(arquivo, aba):
    # pd.read_excel(arquivo,sheet_name="Nome_da_Aba")
    return pd.read_excel(arquivo, sheet_name=aba)

def aguarda_por_id(descricao, id):
    print(f"🕓 Aguardando campo '{descricao}'...")
    return wait.until(EC.presence_of_element_located((By.ID, id)))

def muda_para_iframe():
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])

def preencher_input_por_id(descricao, element_id, texto):
    """Preenche um campo de input por ID."""
    try:
        input_element = aguarda_por_id(descricao, element_id)
        input_element.clear()
        input_element.send_keys(texto)
        print(f"✅ Campo '{descricao}' preenchido com '{texto}'.")
    except TimeoutException:
        _registrar_erro(descricao, element_id)

def preenche_seletor_por_id(descricao, element_id, texto_visivel, tentativas=2, delay=1):
    """Seleciona uma opção visível em um <select> por ID."""
    try:
        aguarda_por_id(descricao, element_id)
        print(f"✅ Campo '{descricao}' localizado.")

        for tentativa in range(tentativas):
            try:
                select_element = driver.find_element(By.ID, element_id)
                Select(select_element).select_by_visible_text(texto_visivel)
                print(f"✅ Opção '{texto_visivel}' selecionada no campo '{descricao}'.")
                return
            except StaleElementReferenceException:
                print(f"⚠️ Tentativa {tentativa + 1} falhou (stale). Retentando após {delay}s...")
                time.sleep(delay)

        print(f"❌ Falha ao selecionar '{texto_visivel}' em '{descricao}' após {tentativas} tentativas.")
    except TimeoutException:
        _registrar_erro(descricao, element_id)

def clicar_botao(texto, type):
    try:
        print(f"🕓 Aguardando botão '{texto}'...")
        botao = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//input[@type="{type}" and @value="{texto}"]')
            )
        )
        try:
            botao.click()
            print(f"✅ Botão '{texto}' clicado com sucesso.")
        except Exception:
            print(f"⚠️ Clique padrão falhou. Usando JavaScript...")
            driver.execute_script("arguments[0].click();", botao)
            print(f"✅ Botão '{texto}' clicado via JavaScript.")
    except TimeoutException:
        print(f"❌ Botão '{texto}' não encontrado.")
        driver.save_screenshot(f"erro_botao_{texto.lower()}.png")

def _registrar_erro(descricao, element_id):
    print(f"❌ Timeout ao localizar o campo '{descricao}' com id='{element_id}'")
    driver.save_screenshot(f"erro_{descricao.lower().replace(' ', '_')}.png")
    with open(f"erro_{descricao.lower().replace(' ', '_')}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    raise TimeoutException(f"Campo '{descricao}' com id='{element_id}' não encontrado.")

def aguarda_por_xpath(descricao, xpath):
    print(f"🕓 Aguardando campo '{descricao}'...")
    try:
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print(f"❌ Timeout ao localizar o campo '{descricao}' (xpath: {xpath})")
        driver.save_screenshot(f"erro_xpath_{descricao.lower().replace(' ', '_')}.png")
        raise

def preencher_input_por_xpath(descricao, xpath, texto):
    aguarda_por_xpath(descricao, xpath)    
    print(f"✅ Campo '{descricao}' localizado.")
    try:
        print(f"🕓 Aguardando campo '{descricao}'...")
        input_element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        input_element.clear()
        input_element.send_keys(texto)
        print(f"✅ Campo '{descricao}' preenchido com '{texto}'.")
    except TimeoutException:
        _registrar_erro(descricao, xpath)

def preenche_seletor_por_xpath(descricao, xpath, texto_visivel, tentativas=2, delay=1):
    try:
        aguarda_por_xpath(descricao, xpath)
        print(f"✅ Campo '{descricao}' localizado.")

        for tentativa in range(tentativas):
            try:
                select_element = driver.find_element(By.XPATH, xpath)
                Select(select_element).select_by_visible_text(texto_visivel)
                print(f"✅ Opção '{texto_visivel}' selecionada no campo '{descricao}'.")
                return
            except StaleElementReferenceException:
                print(f"⚠️ Tentativa {tentativa+1} falhou no campo '{descricao}' (stale). Retentando após {delay}s...")
                time.sleep(delay)

        print(f"❌ Não foi possível selecionar '{texto_visivel}' em '{descricao}' após {tentativas} tentativas.")
    except TimeoutException:
        print(f"❌ Timeout ao localizar o campo '{descricao}'.")
        driver.save_screenshot(f"erro_{descricao.lower().replace(' ', '_')}.png")
        with open(f"erro_{descricao.lower().replace(' ', '_')}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise

def aguardar_login_manual(timeout=1200):
    try:
        print("🕵️ Verificando se é necessário login manual...")

        # Passo 1: Verifica se o botão de login gov.br aparece
        botao_login = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(., "Entrar com") and contains(., "gov.br")]')
            )
        )

        if botao_login.is_displayed():
            print(f"🔒 Login não detectado. Aguardando até {timeout} segundos para que o usuário inicie o login com gov.br...")
            botao_login.click()

            # Passo 2: Espera o campo para digitar o CPF aparecer
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="enter-account-id"]')))
            print("⌨️ Campo para CPF detectado. Aguardando usuário digitar e prosseguir...")

            # Passo 3: Aguarda até o botão de envio aparecer (após o preenchimento do CPF)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit-button"]')))
            print("📨 Botão de envio detectado. Login em andamento...")

        else:
            print("✅ Usuário já está logado (botão de login não visível).")

    except TimeoutException:
        print("⚠️ Elementos de login não apareceram dentro do tempo esperado.")