import time
import subprocess
import sys

import siop_utils
from siop_utils import clicar_botao, aguarda_por_xpath
from siop_utils import preenche_seletor_por_xpath, preencher_input_por_xpath
from siop_utils import get_elemento_xpath, get_url, abrir_excel, muda_para_iframe
from siop_utils import acessa_url

from config import config

def finaliza_navegador():
    try:
        subprocess.run([
            "powershell", "-Command",
            "Stop-Process -Name 'msedge' -Force -ErrorAction SilentlyContinue"
        ], check=True)
        print("🧹 Edge encerrado com sucesso antes da execução.")
    except subprocess.CalledProcessError:
        print("⚠️ Não foi possível encerrar processos do Edge ou nenhum processo estava ativo.")

def seleciona_ano_e_perfil():
    xpath_exercicio = get_elemento_xpath("exercicio")
    aguarda_por_xpath("Exercício", xpath_exercicio)
    preenche_seletor_por_xpath("Exercício", get_elemento_xpath("exercicio"), ano) 
    xpath_perfil = get_elemento_xpath("perfil")
    aguarda_por_xpath("Perfil", xpath_perfil)
    preenche_seletor_por_xpath("Perfil", get_elemento_xpath("perfil"), perfil) 

def listar_objetivo_específico(objetivo):  
    acessa_url(get_url("ppa->objetivo_específico"))
    seleciona_ano_e_perfil()
    muda_para_iframe()
    print("✅ Container principal carregado.")
    preencher_input_por_xpath("Objetivo Específico",
        get_elemento_xpath("ppa.objetivo_especifico.objetivo_especifico_input"), objetivo
    )    
    clicar_botao("Procurar", "submit")    

def listar_objetivos_específicos():  
    acessa_url(get_url("ppa->objetivo_específico"))
    seleciona_ano_e_perfil()
    muda_para_iframe()
    print("✅ Container principal carregado.")
    clicar_botao("Procurar", "submit")  

def exportar_objetivos_específicos():  
    listar_objetivos_específicos()
    aguarda_por_xpath("Tabela Objetivos", get_elemento_xpath("tabela_resultados_objetivos_específicos")) 
    clicar_botao("Exportar...", "button") 

def listar_programa(programa):  
    acessa_url(get_url("ppa->programa"))
    seleciona_ano_e_perfil()
    muda_para_iframe()
    print("✅ Container principal carregado.")
    preencher_input_por_xpath("Programa", get_elemento_xpath("ppa.programa.programa_input"), programa)    
    clicar_botao("Procurar", "submit")    

def listar_programas():  
    acessa_url(get_url("ppa->programa"))
    seleciona_ano_e_perfil()
    muda_para_iframe()
    print("✅ Container principal carregado.")
    clicar_botao("Procurar", "submit")            

def exportar_programas():  
    listar_programas()
    aguarda_por_xpath("Tabela Programas", get_elemento_xpath("tabela_resultados_programas")) 
    clicar_botao("Exportar...", "button") 

def executa_tabela():
    arquivo = "xls/lista.xlsx"
    aba = "Plan1"
    df = abrir_excel(arquivo, aba)

    print(df.head())
    for programa in df["Programa"]:
        print(programa)
        listar_programa(programa)
        time.sleep(1)
        clicar_botao("Limpar", "submit")    
        time.sleep(1)

def main():
    global driver, wait, ano, perfil

    siop_utils.driver, siop_utils.wait = siop_utils.iniciar_driver()
    
    ano = "2025"
    perfil = config.PERFIL_PADRAO
    
    #executa_tabela()   
    #listar_programas()
    #exportar_programas()
    listar_objetivo_específico("0002")
    #listar_objetivos_específicos()
    #exportar_objetivos_específicos()
    #time.sleep(5)
    #listar_programa("1144")

    time.sleep(5)
    siop_utils.driver.quit()

if __name__ == "__main__":
    print ("Iniciando ...")

    resposta = input("\n⚠️ Você precisa estar previamente logado no SIOP.\n\nO navegador Microsoft Edge será fechado. Deseja continuar? (s/n): ").strip().lower()
    if resposta != 's':
        print("Operação cancelada pelo usuário.")
        sys.exit(0)

    finaliza_navegador()
    main()