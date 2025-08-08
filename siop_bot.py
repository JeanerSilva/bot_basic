import siop_utils as sb #siop_bot
import flow

def main():
    sb.define_exercicio("2024")


    # flow.programa("1144")\
    #     .acessa()\
    #     .lista()\
    #     #.exporta()

    # flow.programas()\
    #     .acessa()\
    #     .seleciona_nao_excluido()\
    #     .lista()        
    #     #.exporta()

    # flow.objetivos_especificos()\
    #         .acessa()\
    #         .seleciona_nao_excluido()\
    #         .lista()        \
    #         #.exporta()

    # flow.entregas()\
    #         .acessa()\
    #         .seleciona_nao_excluido()\
    #         .lista()        \
    #         #.exporta()

    flow.entrega("0001")\
        .acessa()\
        .lista()\
        .seleciona_entrega_listada()
    
    sb.espera(5)

    flow.objetivo_especifico("0002")\
       .acessa()\
       .lista()\
       .seleciona_objetivo_listado()\
       .abre_entregas()\
       .clica_link_entrega_por_texto("Encontros anuais com")

    sb.espera(10)
    sb.encerra()

if __name__ == "__main__":
    sb.inicia()