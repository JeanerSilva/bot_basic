import subprocess
import time
import json
import os
import re
import sys


from siop_bot import main
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
    print("Atenção, você precisa já estar logado no SIOP")
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

def get_xpath_elemento_parametrizado(nome_item, **kwargs):
    for elem in _elementos:
        if elem["item"] == nome_item:
            xpath_template = elem.get("xpath")
            if not xpath_template:
                raise ValueError(f"Elemento '{nome_item}' não tem xpath definido.")
            for key, value in kwargs.items():
                xpath_template = xpath_template.replace(f"${{{key}}}", str(value))
            return xpath_template
    raise ValueError(f"Elemento '{nome_item}' não encontrado.")


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
    iframe = aguarda_elemento("Container principal", "//iframe")
    driver.switch_to.frame(iframe)
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

def _registrar_erro(descricao, xpath):
    print(f"❌ Timeout ao localizar o campo '{descricao}' com xpath='{xpath}'")
    driver.save_screenshot(f"erro_{descricao.lower().replace(' ', '_')}.png")
    with open(f"erro_{descricao.lower().replace(' ', '_')}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    raise TimeoutException(f"Campo '{descricao}' com xpath='{xpath}' não encontrado.")

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
                print("✅ Ações do jQuery encerradas.")
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
            print(f"✅ Campo '{descricao}' carregado e ações do jQuery já encerradas.")
        else:
            aguarda_dom()
            print(f"✅ Campo '{descricao}' carregado e ações do DOM já encerradas.")        
        return elemento
    except TimeoutException:
        print(f"❌ Timeout ao localizar o campo '{descricao}' (xpath: {xpath})")
        driver.save_screenshot(f"erro_xpath_{descricao.lower().replace(' ', '_')}.png")
        raise

def aguarda_texto_no_elemento(descricao, xpath, texto):
    print(f"🕓 Aguardando campo '{descricao}'...")
    try:
        elemento = wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath), texto))
        if jquery:
            aguarda_jquery()  # nova adição
            print(f"✅ Campo '{descricao}' carregado e ações do jQuery já encerradas.")
        else:
            aguarda_dom()
            print(f"✅ Campo '{descricao}' carregado e ações do DOM já encerradas.")        
        return elemento
    except TimeoutException:
        print(f"❌ Timeout ao localizar o campo '{descricao}' (xpath: {xpath})")
        driver.save_screenshot(f"erro_xpath_{descricao.lower().replace(' ', '_')}.png")
        raise


def clica_link(descricao, elemento, _numero=0):
    if _numero == 0:
        xpath = get_xpath_elemento(elemento)
    else:
        xpath = get_xpath_elemento_parametrizado(elemento, numero=_numero)
    try:
        elemento = aguarda_elemento(descricao, xpath)  
        elemento.click()
        print("✅ Link clicado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao clicar no link: {e}")

def clica_link_por_texto_inicial(texto_inicial):
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

from selenium.common.exceptions import StaleElementReferenceException

def clica_item_painel(descricao_painel, item_painel, descricao_link, item_link):
    painel_xpath = get_xpath_elemento(item_painel)
    aguarda_elemento(descricao_painel, painel_xpath)

    link_xpath = painel_xpath + get_xpath_elemento(item_link)
    link = aguarda_elemento(descricao_link, link_xpath)

    driver.execute_script("arguments[0].scrollIntoView(true);", link)
    driver.execute_script("arguments[0].click();", link)
    print(f"✅ {descricao_link} clicado com sucesso.")

def preenche_input(descricao, elemento, texto):
    xpath = get_xpath_elemento(elemento)
    try:
        input_element = aguarda_elemento(descricao, xpath)  # já espera e retorna
        print(f"✅ Campo '{descricao}' localizado.")
        input_element.clear()
        input_element.send_keys(texto)
        print(f"✅ Campo '{descricao}' preenchido com '{texto}'.")
    except StaleElementReferenceException:
        print(f"⚠️ Elemento '{descricao}' ficou obsoleto. Tentando localizar novamente...")
        input_element = aguarda_elemento(descricao, xpath)  # busca de novo
        input_element.clear()
        input_element.send_keys(texto)
        print(f"✅ Campo '{descricao}' preenchido após nova tentativa.")
    except Exception:
        _registrar_erro(descricao, xpath)

def preenche_input_file(descricao, elemento, texto):
    xpath = get_xpath_elemento(elemento)
    try:
        input_element = aguarda_elemento(descricao, xpath)  # já espera e retorna
        print(f"✅ Campo '{descricao}' localizado.")
        input_element.send_keys(texto)
        print(f"✅ Campo '{descricao}' preenchido com '{texto}'.")
    except StaleElementReferenceException:
        print(f"⚠️ Elemento '{descricao}' ficou obsoleto. Tentando localizar novamente...")
        input_element = aguarda_elemento(descricao, xpath)  # busca de novo
        input_element.send_keys(texto)
        print(f"✅ Campo '{descricao}' preenchido após nova tentativa.")
    except Exception:
        _registrar_erro(descricao, xpath)


def preenche_seletor(descricao, xpath, texto_visivel, tentativas=3, delay=2):
    for tentativa in range(1, tentativas + 1):
        try:
            print(f"🕓 Tentativa {tentativa} - aguardando campo '{descricao}' para preencer com {texto_visivel}...")
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

def seleciona_seletor(descricao, elemento, texto_visivel):
    xpath = get_xpath_elemento(elemento)
    aguarda_elemento(descricao, xpath)
    preenche_seletor(descricao, xpath, texto_visivel)

def encerra():
    driver.quit()

def inicia():
    if len(sys.argv) > 1 and sys.argv[1].lower() == '/y':
        print ("Iniciando ...")
        finaliza_navegador()
        iniciar_driver()
        main()
    else:
        resposta = input("\n⚠️ Você precisa estar previamente logado no SIOP.\n\nO navegador Microsoft Edge será fechado. Deseja continuar? (s/n): ").strip().lower()
        if resposta != 's':
            print("Operação cancelada pelo usuário.")
        else:    
            finaliza_navegador()
            iniciar_driver()
            main()


def define_exercicio(novo_ano=None):
    global ano  # permite modificar a variável global

    if novo_ano:
        ano = novo_ano
        print(f"✅ Ano definido como '{ano}' via argumento.")

def espera(tempo):
    print(f"🕓 Aguardando {tempo} segundos ...")
    for i in range(tempo):
        print(f"\r⏳ {i + 1}/{tempo} segundos", end='', flush=True)
        time.sleep(1)
    print("\n✅ Concluído.")

def finaliza_navegador():
    print ("🕓 Verificando se o navegador está aberto ...")
    try:
        subprocess.run([
            "powershell", "-Command",
            "Stop-Process -Name 'msedge' -Force -ErrorAction SilentlyContinue"
        ], check=True)
        print("🧹 Edge encerrado com sucesso antes da execução.")
    except subprocess.CalledProcessError:
        print("⚠️ Não foi possível encerrar processos do Edge ou nenhum processo estava ativo.")

def extrai_numero_pac(nome_arquivo: str) -> int | None:
    m = re.search(r'PAC[^0-9]*([0-9]+)', nome_arquivo, flags=re.IGNORECASE)
    return int(m.group(1)) if m else None

def monta_objetivo(n: int) -> str:
    return f"{n:04d}"

def debug_contexto(sb, limite=15, mostrar_html_inicio=False):
    script = r"""
    const max = arguments[0] || 15;
    const all = document.querySelectorAll('*');
    const res = [];
    const inIframe = (window.self !== window.top);
    res.push({
        tipo: '__header__',
        contexto: inIframe ? 'iframe' : 'default_content',
        frameId: inIframe && window.frameElement ? window.frameElement.id || null : null,
        frameName: inIframe && window.frameElement ? window.frameElement.name || null : null,
        titulo: document.title || '',
        url: location.href,
        total: all.length
    });
    const n = Math.min(max, all.length);
    for (let i = 0; i < n; i++) {
        const e = all[i];
        res.push({
            tag: e.tagName.toLowerCase(),
            id: e.id || '',
            class: (e.className && e.className.toString) ? e.className.toString() : '',
            text: (e.textContent || '').trim().slice(0, 120)
        });
    }
    return res;
    """
    data = sb.driver.execute_script(script, int(limite))
    header = data[0]
    print(f"🔎 DOM atual: total={header['total']} elementos | contexto={header['contexto']} | "
          f"frameId={header['frameId']} | frameName={header['frameName']}")
    # Lista amostra
    for i, row in enumerate(data[1:], start=1):
        print(f"{i:02d}. <{row['tag']} id='{row['id']}' class='{row['class']}'>  txt='{row['text']}'")

def contexto_atual(sb):
    frame = sb.driver.execute_script("return self.frameElement")
    if frame is None:
        print("🧭 Contexto: default_content (página principal).")
        return {"contexto": "default_content", "frame_id": None, "frame_name": None}
    else:
        info = {
            "contexto": "iframe",
            "frame_id": frame.get_attribute("id"),
            "frame_name": frame.get_attribute("name"),
        }
        print(f"🧭 Contexto: iframe id={info['frame_id']} name={info['frame_name']}")
        return info