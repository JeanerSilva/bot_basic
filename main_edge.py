import time
import sys
import siop_utils as sb #siop_bot
from config.config import JQUERY

def lista_objetivo_específico(objetivo):  
    sb.acessa("ppa->objetivo_específico")
    sb.seleciona_ano_e_perfil_e_muda_de_frame()    
    sb.preenche_input("Objetivo Específico", "ppa.objetivo_especifico.objetivo_especifico_input", objetivo)    
    sb.clica_botao("Procurar", "submit")    

def lista_objetivos_específicos():  
    sb.acessa("ppa->objetivo_específico")
    sb.seleciona_ano_e_perfil_e_muda_de_frame()
    sb.clica_botao("Procurar", "submit")  

def seleciona_primeiro_objetivo_listado (descricao, xpath):        
    sb.clicar_link(descricao, xpath)    

def exporta_objetivos_específicos():  
    lista_objetivos_específicos()
    sb.aguarda_elemento("Tabela Objetivos", "tabela_resultados_objetivos_específicos", JQUERY) 
    sb.clica_botao("Exportar...", "button") 

def lista_programa(programa):  
    sb.acessa("ppa->programa")
    sb.seleciona_ano_e_perfil_e_muda_de_frame()
    sb.preenche_input("Programa", "ppa.programa.programa_input", programa)    
    sb.clica_botao("Procurar", "submit")    

def lista_programas():  
    sb.acessa("ppa->programa")
    sb.seleciona_ano_e_perfil_e_muda_de_frame()
    sb.clica_botao("Procurar", "submit")            

def exporta_programas():  
    lista_programas()
    sb.aguarda_elemento("Tabela Programas", "tabela_resultados_programas", JQUERY)
    sb.clica_botao("Exportar...", "button") 

def executa_tabela():
    arquivo = "xls/lista.xlsx"
    aba = "Plan1"
    df = sb.abrir_excel(arquivo, aba)

    print(df.head())
    for programa in df["Programa"]:
        print(programa)
        lista_programa(programa)
        time.sleep(1)
        sb.clica_botao("Limpar", "submit")    
        time.sleep(1)

def insere_nota_do_usuario_em_objetivo_especifico (objetivo, nota):
    lista_objetivo_específico(objetivo)    
    seleciona_primeiro_objetivo_listado("Seleciona primeiro objetivo", "tabela_resultados_objetivos_específicos.primeiro_item")
    sb.preenche_input("Nota do usuário", "objetivo_especifico.informacoes_basicas.nota_do_usuario", nota)      

def abre_indicador_do_objetivo_especifico (objetivo):
    lista_objetivo_específico(objetivo)    
    seleciona_primeiro_objetivo_listado("Seleciona primeiro objetivo", "tabela_resultados_objetivos_específicos.primeiro_item")
    sb.clicar_link("Botão Indicadores", "objetivo_especifico.botao_indicadores")
    sb.clicar_link("Indicador do objetivo", "objetivo_especifico.botao_indicadores.indicador")

def main():
    sb.iniciar_driver()
    sb.ano = "2024"
    sb.jquery = JQUERY

    #executa_tabela()   
    #lista_programas()
    #exporta_programas()
    #lista_objetivo_específico("0002")  
    #insere_nota_do_usuario_em_objetivo_especifico ("0002", "teste")
    abre_indicador_do_objetivo_especifico ("0002")
    #lista_objetivos_específicos()
    #exporta_objetivos_específicos()
    #lista_programa("1144")
    time.sleep(1)
    #sb.clica_na_tela_e_digita (598, 52, "teste")

    #time.sleep(5)
    sb.driver.quit()

if __name__ == "__main__":
    print ("Iniciando ...")
    if len(sys.argv) > 1 and sys.argv[1].lower() == '/y':
        print("🟢 Início automático com argumento '/y'")
        sb.finaliza_navegador()
        main()
    else:
        resposta = input("\n⚠️ Você precisa estar previamente logado no SIOP.\n\nO navegador Microsoft Edge será fechado. Deseja continuar? (s/n): ").strip().lower()
        if resposta != 's':
            print("Operação cancelada pelo usuário.")
        else:    
            sb.finaliza_navegador()
            main()