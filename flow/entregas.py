import siop_utils as sb

class entregas:
    def acessa(self):
        sb.acessa("ppa->entrega")
        sb.seleciona_ano_e_perfil_e_muda_de_frame()
        return self

    def lista(self):
        sb.clica_botao_tipo("Procurar", "submit")
        return self

    def limpa(self):
        sb.clica_botao_tipo("Limpar", "submit")
        return self
    
    def seleciona_nao_excluido(self):
        sb.seleciona_seletor("Não excluído", "entrega.nao_excluído", "Não Excluído")
        return self

    def exporta(self):
        sb.aguarda_tabela("Tabela Entregas", "tabela_resultados_programas")
        sb.clica_botao_tipo("Exportar...", "button")
        return self
