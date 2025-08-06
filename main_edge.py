import time
import siop_utils as sb #siop_bot

def listar_objetivo_específico(objetivo):  
    sb.acessa_url("ppa->objetivo_específico")
    sb.seleciona_ano_e_perfil()
    sb.muda_para_iframe()
    print("✅ Container principal carregado.")
    sb.preencher_input_por_xpath("Objetivo Específico", "ppa.objetivo_especifico.objetivo_especifico_input", objetivo)    
    sb.clicar_botao("Procurar", "submit")    

def listar_objetivos_específicos():  
    sb.acessa_url("ppa->objetivo_específico")
    sb.seleciona_ano_e_perfil()
    sb.muda_para_iframe()
    print("✅ Container principal carregado.")
    sb.clicar_botao("Procurar", "submit")  

def exportar_objetivos_específicos():  
    listar_objetivos_específicos()
    sb.aguarda_por_xpath("Tabela Objetivos", "tabela_resultados_objetivos_específicos") 
    sb.clicar_botao("Exportar...", "button") 

def listar_programa(programa):  
    sb.acessa_url("ppa->programa")
    sb.seleciona_ano_e_perfil()
    sb.muda_para_iframe()
    print("✅ Container principal carregado.")
    sb.preencher_input_por_xpath("Programa", "ppa.programa.programa_input", programa)    
    sb.clicar_botao("Procurar", "submit")    

def listar_programas():  
    sb.acessa_url("ppa->programa")
    sb.seleciona_ano_e_perfil()
    sb.muda_para_iframe()
    print("✅ Container principal carregado.")
    sb.clicar_botao("Procurar", "submit")            

def exportar_programas():  
    listar_programas()
    sb.aguarda_por_xpath("Tabela Programas", "tabela_resultados_programas")
    sb.clicar_botao("Exportar...", "button") 

def executa_tabela():
    arquivo = "xls/lista.xlsx"
    aba = "Plan1"
    df = sb.abrir_excel(arquivo, aba)

    print(df.head())
    for programa in df["Programa"]:
        print(programa)
        listar_programa(programa)
        time.sleep(1)
        sb.clicar_botao("Limpar", "submit")    
        time.sleep(1)

def main():
    global driver, wait
    sb.driver, sb.wait = sb.iniciar_driver()
    sb.ano = "2025"
   
    #executa_tabela()   
    listar_programas()
    #exportar_programas()
    #listar_objetivo_específico("0002")
    #listar_objetivos_específicos()
    #exportar_objetivos_específicos()
    #time.sleep(5)
    #listar_programa("1144")

    time.sleep(5)
    sb.driver.quit()

if __name__ == "__main__":
    print ("Iniciando ...")
    resposta = input("\n⚠️ Você precisa estar previamente logado no SIOP.\n\nO navegador Microsoft Edge será fechado. Deseja continuar? (s/n): ").strip().lower()
    if resposta != 's':
        print("Operação cancelada pelo usuário.")
    else:    
        sb.finaliza_navegador()
        main()