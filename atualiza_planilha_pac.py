import siop_utils as sb #siop_bot
import flow

def main():
    
    # Atualização de PAC 2024 (sem apagar arquivo antes)
    flow.atualizar_pac_em_lote(
        exercicio="2024",
        pasta=r"C:\SEPLAN\Planilhas xls para alteração SIOP\teste\Dezembro - 2024 - Original\amostra",
        data_referencia="31/12/2024",
        reiniciar_driver_entre_arquivos=True,
        apaga_antes=False,
    )
        

    # Atualização de PAC em lote (fluxo padronizado)
    # flow.atualizar_pac_em_lote(
    #     exercicio="2025",
    #     pasta=r"C:\SEPLAN\siop-bot\xls\altera\Abril - 2025",
    #     data_referencia="30/04/2025",
    #     reiniciar_driver_entre_arquivos=True,
    # )

    

    sb.espera(1)
    sb.encerra()

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

    # flow.entrega("0001")\
    #     .acessa()\
    #     .lista()\
    #     .seleciona_entrega_listada()
    
    # sb.espera(5)

    # flow.objetivo_especifico("0002")\
    #     .acessa()\
    #     .lista()\
    #     .seleciona_objetivo_listado()\
    #     .abre_indicadores()


    # flow.objetivo_especifico("0105")\
    #     .acessa()\
    #     .lista()\
    #     .seleciona_objetivo_listado()\
    #     .abre_entregas()\
    #     .clica_link_entrega_por_texto("Encontros anuais com")
    
    # os.makedirs("prints", exist_ok=True)

if __name__ == "__main__":
    sb.inicia() 