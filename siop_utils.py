import subprocess
import time
import json
import os
import re

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd

from config import config

driver = None
wait = None
ano = config.ANO_PADRAO
perfil = config.PERFIL_PADRAO
jquery = True
BASE_DIR = config.BASE_DIR

def iniciar_driver(tentativas=3, delay=5):
    global driver, wait, actions
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
    edge_options.add_argument(f'--profile-directory={config.PERFIL_EDGE_PADRAO}')

    for tentativa in range(1, tentativas + 1):
        try:
            print(f"🚀 Tentativa {tentativa} de iniciar o Edge...")
            driver = webdriver.Edge(service=service, options=edge_options)
            wait = WebDriverWait(driver, 120)
            actions = ActionChains(driver)
            print("✅ Edge iniciado com sucesso.")
            return driver, wait
        except SessionNotCreatedException as e:
            print(f"❌ Erro ao iniciar Edge (tentativa {tentativa}): {e}")
            time.sleep(delay)    
    raise RuntimeError("❌ Falha ao iniciar o Edge após múltiplas tentativas.")    

# Carrega os elementos do JSON uma vez
with open(os.path.join(BASE_DIR, "config/elementos.json"), "r", encoding="utf-8") as f:
    _elementos = json.load(f)

with open(os.path.join(BASE_DIR, "config/urls.json"), "r", encoding="utf-8") as f:
    _urls = json.load(f)

def get_xpath_elemento(elemento):
    tipo = "xpath"
    for elem in _elementos:
        if elem["item"] == elemento:
            return elem.get(tipo)
    raise ValueError(f"Elemento '{elemento}' com tipo '{tipo}' não encontrado.")

def get_url(atividade):
    for item in _urls:
        if item["atividade"] == atividade:
            return item["url"]
    raise ValueError(f"URL para atividade '{atividade}' não encontrada.")

def clica_na_tela(x,y):    
    actions.move_by_offset(x, y).click().perform()

def digita(texto):
    actions.send_keys(texto).perform()

def clica_na_tela_e_digita(x,y, texto):    
    actions.move_by_offset(x, y).click().send_keys(texto).perform()

def acessa(url):
    driver.get(config.URL_BASE + get_url(url))

def abrir_excel(arquivo, aba):
    # pd.read_excel(arquivo,sheet_name="Nome_da_Aba")
    return pd.read_excel(arquivo, sheet_name=aba)

def navega_para_painel():
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
    print("✅ Container principal carregado.")

def clica_botao_tipo(texto, type):
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

def aguarda_dom(timeout=10):
    print("🕓 Aguardando document.readyState = 'complete'...")
    for _ in range(timeout * 2):  # verifica a cada 0.5s
        try:
            pronto = driver.execute_script("return document.readyState === 'complete';")
            if pronto:
                print("✅ DOM completamente carregado.")
                return
        except Exception as e:
            print(f"⚠️ Erro ao verificar readyState (ignorado): {e}")
        time.sleep(0.5)
    print("⚠️ DOM não ficou pronto após timeout.")


def aguarda_jquery(timeout=10):
    print("🕓 Aguardando jQuery ficar inativo ou ausente...")
    for i in range(timeout * 2):  # verifica a cada 0.5s
        try:
            pronto = driver.execute_script("""
                return (
                    typeof jQuery === 'undefined' || 
                    (typeof jQuery.active !== 'undefined' && jQuery.active === 0)
                );
            """)
            if pronto:
                print("✅ jQuery ausente ou inativo.")
                return
        except Exception as e:
            print(f"⚠️ Erro ao verificar jQuery (ignorado): {e}")
        time.sleep(0.5)
    print("⚠️ jQuery ainda ativo (ou script falhou) após timeout.")

def aguarda_tabela(descricao, tabela):
    xpath = get_xpath_elemento(tabela)
    aguarda_elemento(descricao, xpath)

def aguarda_elemento(descricao, xpath):
    print(f"🕓 Aguardando campo '{descricao}'...")
    try:
        elemento = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        if jquery:
            aguarda_jquery()  # nova adição
        else:
            aguarda_dom()
        print(f"✅ Campo '{descricao}' carregado e jQuery inativo.")
        return elemento
    except TimeoutException:
        print(f"❌ Timeout ao localizar o campo '{descricao}' (xpath: {xpath})")
        driver.save_screenshot(f"erro_xpath_{descricao.lower().replace(' ', '_')}.png")
        raise

def clica_link(descricao, elemento):
    xpath = get_xpath_elemento(elemento)
    try:
        elemento = aguarda_elemento(descricao, xpath)  
        elemento.click()
        print("✅ Link clicado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao clicar no link: {e}")

def clica_link_por_texto_inicial(texto_inicial, timeout=10):
    print(f"🕓 Procurando link que começa com: '{texto_inicial}'...")
    xpath = f"//a[starts-with(normalize-space(text()), '{texto_inicial}')]"

    try:
        link = aguarda_elemento(f"Link '{texto_inicial}'", xpath)  # usa sua função
        try:
            link.click()
            print("✅ Link clicado com sucesso.")
        except Exception as e:
            mensagem_curta = str(e).split("\n")[0]  # extrai apenas a primeira linha
            print(f"⚠️ Clique normal falhou: {mensagem_curta}")
            driver.execute_script("arguments[0].click();", link)
            print("✅ Link clicado via JavaScript.")
    except Exception as e:
        print(f"❌ Erro ao localizar ou clicar no link: {e}")

def preenche_input(descricao, elemento, texto):
    xpath = get_xpath_elemento(elemento)
    aguarda_elemento(descricao, xpath)    
    print(f"✅ Campo '{descricao}' localizado.")
    try:
        print(f"🕓 Aguardando campo '{descricao}'...")
        input_element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        input_element.clear()
        input_element.send_keys(texto)
        print(f"✅ Campo '{descricao}' preenchido com '{texto}'.")
    except TimeoutException:
        _registrar_erro(descricao, xpath)

def preenche_seletor(descricao, xpath, texto_visivel, tentativas=3, delay=2):
    for tentativa in range(1, tentativas + 1):
        try:
            print(f"🕓 Tentativa {tentativa} - aguardando campo '{descricao}'...")
            aguarda_elemento(descricao, xpath)
            print(f"✅ Campo '{descricao}' localizado.")
            
            select_element = driver.find_element(By.XPATH, xpath)
            Select(select_element).select_by_visible_text(texto_visivel)
            print(f"✅ Opção '{texto_visivel}' selecionada no campo '{descricao}'.")
            return  # sucesso, sai da função
        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"⚠️ Tentativa {tentativa} falhou ao preencher '{descricao}': {type(e).__name__}")
            time.sleep(delay)
        except TimeoutException:
            print(f"❌ Timeout ao localizar o campo '{descricao}' (xpath: {xpath})")
            driver.save_screenshot(f"erro_{descricao.lower().replace(' ', '_')}.png")
            with open(f"erro_{descricao.lower().replace(' ', '_')}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            raise
        except Exception as e:
            print(f"❌ Erro inesperado na tentativa {tentativa} ao preencher '{descricao}': {e}")
            time.sleep(delay)

    raise RuntimeError(f"❌ Falha ao selecionar '{texto_visivel}' no campo '{descricao}' após {tentativas} tentativas.")

def seleciona_ano_e_perfil_e_muda_de_frame():
    xpath_exercicio = get_xpath_elemento("exercicio")
    aguarda_elemento("Exercício", xpath_exercicio)
    preenche_seletor("Exercício", xpath_exercicio, ano)
    xpath_perfil = get_xpath_elemento("perfil")
    aguarda_elemento("Perfil", xpath_perfil)
    preenche_seletor("Perfil", xpath_perfil, perfil)
    navega_para_painel()    

def finaliza_navegador():
    try:
        subprocess.run([
            "powershell", "-Command",
            "Stop-Process -Name 'msedge' -Force -ErrorAction SilentlyContinue"
        ], check=True)
        print("🧹 Edge encerrado com sucesso antes da execução.")
    except subprocess.CalledProcessError:
        print("⚠️ Não foi possível encerrar processos do Edge ou nenhum processo estava ativo.")