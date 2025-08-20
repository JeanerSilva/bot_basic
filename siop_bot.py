import siop_utils as sb #siop_bot
import flow

def main():
    
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


    # exercicio = "2024"
    # sb.define_exercicio(exercicio)    
    # #path = r"C:\SEPLAN\siop-bot\xls\altera"
    # path = r"C:\SEPLAN\siop-bot\xls\altera\Dezembro - 2024"
    # arquivos = sorted(Path(path).glob("*.xlsx"))
    # if not arquivos:
    #     print("⚠️ Nenhum arquivo encontrado.")
    #     return
    # for arq in arquivos:
    #     if arq.name.startswith("enviado."):
    #         continue
    #     num = sb.extrai_numero_pac(arq.name)
    #     if num is None:
    #         continue
    #     objetivo = sb.monta_objetivo(num)  # ajuste aqui se sua regra for diferente
    #     arquivo = path + "\\" + arq.name
    #     flow.objetivo_especifico(objetivo)\
    #      .acessa()\
    #      .lista()\
    #      .seleciona_objetivo_listado()\
    #      .adiciona_arquivo_pac(f"OE {objetivo}: Ações do Novo PAC (Data de referência: 31/12/2024).", arquivo, objetivo, exercicio)
        
                        
    #     novo_nome = arq.with_name(f"enviado.{arq.name}")
    #     try:
    #         arq.rename(novo_nome)
    #         print(f"✅ Arquivo renomeado: {novo_nome}")
    #     except Exception as e:
    #         print(f"⚠️ Não consegui renomear {arq.name}: {e}")                                 
    #     sb.encerra()
    #     sb.finaliza_navegador()
    #     sb.iniciar_driver()
        

    # Atualização de PAC em lote (fluxo padronizado)
    flow.atualizar_pac_em_lote(
        exercicio="2025",
        pasta=r"C:\SEPLAN\siop-bot\xls\altera\Abril - 2025",
        data_referencia="30/04/2025",
        reiniciar_driver_entre_arquivos=True,
    )

    

    sb.espera(10)
    sb.encerra()

if __name__ == "__main__":
    sb.inicia() 