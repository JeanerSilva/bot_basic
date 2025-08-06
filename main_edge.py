import time
import siop_utils as siop_bot

def listar_objetivo_específico(objetivo):  
    siop_bot.acessa_url(siop_bot.get_url("ppa->objetivo_específico"))
    siop_bot.seleciona_ano_e_perfil()
    siop_bot.muda_para_iframe()
    print("✅ Container principal carregado.")
    siop_bot.preencher_input_por_xpath("Objetivo Específico", siop_bot.get_elemento_xpath("ppa.objetivo_especifico.objetivo_especifico_input"), objetivo)    
    siop_bot.clicar_botao("Procurar", "submit")    

def listar_objetivos_específicos():  
    siop_bot.acessa_url(siop_bot.get_url("ppa->objetivo_específico"))
    siop_bot.seleciona_ano_e_perfil()
    siop_bot.muda_para_iframe()
    print("✅ Container principal carregado.")
    siop_bot.clicar_botao("Procurar", "submit")  

def exportar_objetivos_específicos():  
    listar_objetivos_específicos()
    siop_bot.aguarda_por_xpath("Tabela Objetivos", siop_bot.get_elemento_xpath("tabela_resultados_objetivos_específicos")) 
    siop_bot.clicar_botao("Exportar...", "button") 

def listar_programa(programa):  
    siop_bot.acessa_url(siop_bot.get_url("ppa->programa"))
    siop_bot.seleciona_ano_e_perfil()
    siop_bot.muda_para_iframe()
    print("✅ Container principal carregado.")
    siop_bot.preencher_input_por_xpath("Programa", siop_bot.get_elemento_xpath("ppa.programa.programa_input"), programa)    
    siop_bot.clicar_botao("Procurar", "submit")    

def listar_programas():  
    siop_bot.acessa_url(siop_bot.get_url("ppa->programa"))
    siop_bot.seleciona_ano_e_perfil()
    siop_bot.muda_para_iframe()
    print("✅ Container principal carregado.")
    siop_bot.clicar_botao("Procurar", "submit")            

def exportar_programas():  
    listar_programas()
    siop_bot.aguarda_por_xpath("Tabela Programas", siop_bot.get_elemento_xpath("tabela_resultados_programas")) 
    siop_bot.clicar_botao("Exportar...", "button") 

def executa_tabela():
    arquivo = "xls/lista.xlsx"
    aba = "Plan1"
    df = siop_bot.abrir_excel(arquivo, aba)

    print(df.head())
    for programa in df["Programa"]:
        print(programa)
        listar_programa(programa)
        time.sleep(1)
        siop_bot.clicar_botao("Limpar", "submit")    
        time.sleep(1)

def main():
    global driver, wait
    siop_bot.driver, siop_bot.wait = siop_bot.iniciar_driver()
    siop_bot.ano = "2025"
   
    #executa_tabela()   
    #listar_programas()
    #exportar_programas()
    listar_objetivo_específico("0002")
    #listar_objetivos_específicos()
    #exportar_objetivos_específicos()
    #time.sleep(5)
    #listar_programa("1144")

    time.sleep(5)
    siop_bot.driver.quit()

if __name__ == "__main__":
    print ("Iniciando ...")
    resposta = input("\n⚠️ Você precisa estar previamente logado no SIOP.\n\nO navegador Microsoft Edge será fechado. Deseja continuar? (s/n): ").strip().lower()
    if resposta != 's':
        print("Operação cancelada pelo usuário.")
    else:    
        siop_bot.finaliza_navegador()
        main()