import sys
import siop_utils as sb #siop_bot
import flow

def main():
    sb.define_exercicio("2024")

    flow.ObjetivoEspecificoFlow("0002")\
       .acessa()\
       .lista()\
       .seleciona_objetivo_listado()\
       .abre_entregas()\
       .clica_link_entrega_por_texto("Encontros anuais com")

    # flow.ProgramaFlow("1144")\
    #     .acessa()\
    #     .lista()\
    #     .exporta()

    sb.espera(10)
    sb.encerra()

if __name__ == "__main__":
    sb.inicia()