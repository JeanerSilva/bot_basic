from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
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
import shutil
import sys




def copiar_perfil_chrome(origem='Profile 2', destino_final='C:\\SEPLAN\\chrome_perfil_selenium'):
    base_user_data = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
    caminho_origem = os.path.join(base_user_data, origem)

    if not os.path.exists(caminho_origem):
        print(f"❌ Perfil de origem não encontrado: {caminho_origem}")
        sys.exit(1)

    # Se já existir o destino, remove para recriar
    if os.path.exists(destino_final):
        print(f"🧹 Limpando pasta de destino existente: {destino_final}")
        shutil.rmtree(destino_final)

    print(f"📂 Copiando perfil de:\n  {caminho_origem}\npara:\n  {destino_final}")
    shutil.copytree(caminho_origem, os.path.join(destino_final, 'Default'))

    print("✅ Cópia concluída com sucesso.")

def finaliza_navegador():
    # Finaliza instâncias anteriores do Chrome
    try:
        subprocess.run([
            "powershell", "-Command",
            "Stop-Process -Name 'chrome' -Force -ErrorAction SilentlyContinue"
        ], check=True)
        print("🧹 Chrome encerrado com sucesso antes da execução.")
    except subprocess.CalledProcessError:
        print("⚠️ Não foi possível encerrar processos do Chrome ou nenhum processo estava ativo.")

def copia_perfil():
    copiar_perfil_chrome(origem='Profile 2', destino_final='C:\\SEPLAN\\chrome_perfil_selenium')

def iniciar_driver():
    chrome_options = Options()
    #caminho = os.path.expandvars(r'%LOCALAPPDATA%\\Google\\Chrome\\User Data')
    caminho = os.path.expandvars(r'c:\\SEPLAN\\selenium_siop-main')
    caminho_ajustado = re.sub(r'\\+', r'\\\\', caminho) 
    print(f"Caminho: {caminho_ajustado}")
    argumento = f'--user-data-dir={caminho_ajustado}'
    chrome_options.add_argument(argumento)
    chrome_options.add_argument('--profile-directory=Profile 2')
    chrome_options.add_argument("--log-level=3")  # 3 suprime 0 é DEBUG


    return webdriver.Chrome(options=chrome_options)  # alterado para Chrome

# O restante do código permanece igual
def main():
    driver = iniciar_driver()
    wait = WebDriverWait(driver, 120)
    driver.get("https://www.siop.planejamento.gov.br/modulo/main/index.html#/150")

    #aguardar_login_manual(wait, driver)

    preenche_seletor_por_xpath(driver, wait, "Exercício", '//label[contains(text(), "Exercício")]/following-sibling::div/select', "2025")
    preenche_seletor_por_xpath(driver, wait, "Perfil", '//label[contains(text(), "Perfil")]/following-sibling::div/select', "Controle de Qualidade - SEPLAN")

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
    
    print("✅ Container principal carregado.")

    #preencher_input_por_id(driver, wait, "Objetivo Específico",
    #    "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:txtPesquisaObjetivoCodigo", "1144"
    #)

    preencher_input_por_xpath(driver, wait, "Objetivo Específico",
        '//*[@id="form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:txtPesquisaObjetivoCodigo"]', "1144"
    )

    preenche_seletor_por_id(driver, wait, "Programa",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoPrograma",
        "1144 - Agropecuária Sustentável"
    )
    preenche_seletor_por_id(driver, wait, "Órgão",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoOrgao",
        "22000 - Ministério da Agricultura e Pecuária"
    )
    preenche_seletor_por_id(driver, wait, "Origem",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoTipoInclusao", "PPA"
    )
    preenche_seletor_por_id(driver, wait, "Momento",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoMomento", "Base de Partida"
    )
    preenche_seletor_por_id(driver, wait, "Alterado",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoAlterado", "Alterado"
    )
    preenche_seletor_por_id(driver, wait, "Excluído",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoExcluido", "Não Excluído"
    )
    preenche_seletor_por_id(driver, wait, "Novo",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoNovo", "Novo"
    )
    preenche_seletor_por_id(driver, wait, "Validado",
        "form:subTelaPesquisa:subTelaPesquisaObjetivoEspecifico:cmbPesquisaObjetivoValidado", "Validado"
    )

    clicar_botao(driver, wait, texto="Procurar")

    time.sleep(20)
    driver.quit()

if __name__ == "__main__":

    if '--recrie' in sys.argv:
        copiar_perfil_chrome()
    else:
        print("ℹ️ Argumento '--recrie' não fornecido. Mantendo o perfil existente.")  
        
    #finaliza_navegador()
    #main()
    print(get_elemento("ppa.programa.programa_input", "xpath"))
    print(get_url("listar_objetivo_específico"))


#[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\SEPLAN\selenium_siop-main\drivers\chrome", "Machine")
