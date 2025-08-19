import siop_utils as sb

class objetivos_especificos:

    def acessa(self):
        sb.acessa("ppa->objetivo_específico")
        sb.seleciona_ano_e_perfil_e_muda_de_frame()
        return self

    def seleciona_nao_excluido(self):
        sb.seleciona_seletor("Não excluído", "objetivo.nao_excluído", "Não Excluído")
        return self

    def lista(self):
        sb.clica_botao_tipo("Procurar", "submit")
        return self

    def seleciona_objetivo_listado(self):
        sb.clica_link("Primeiro objetivo", "tabela_resultados_objetivos_específicos.primeiro_item", self.objetivo)
        return self

    def exporta(self):
        sb.aguarda_tabela("Tabela Objetivos Específicos", "tabela_resultados_objetivos_específicos")
        sb.clica_botao_tipo("Exportar...", "button")
        return self
    
   