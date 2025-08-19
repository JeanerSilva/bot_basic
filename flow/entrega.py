import siop_utils as sb

class entrega:
    def __init__(self, codigo_entrega: str):
        if not codigo_entrega or not str(codigo_entrega).strip():
            raise ValueError("❌ Parâmetro 'codigo_entrega' é obrigatório e não pode estar vazio.")
        self.codigo_entrega = codigo_entrega

    def acessa(self):
        sb.acessa("ppa->entrega")
        sb.seleciona_ano_e_perfil_e_muda_de_frame("ppa.entrega.entrega_input")
        return self

    def lista(self):
        sb.preenche_input("Entrega", "ppa.entrega.entrega_input", self.codigo_entrega)
        sb.clica_botao_tipo("Procurar", "submit")
        return self
    
    def seleciona_entrega_listada(self):
        sb.clica_link("Primeira entrega", "tabela_resultados_entrega.primeiro_item", self.codigo_entrega)
        return self

    def limpa(self):
        sb.clica_botao_tipo("Limpar", "submit")
        return self

    def exporta(self):
        sb.aguarda_tabela("Tabela Enregas", "tabela_resultados_entregas")
        sb.clica_botao_tipo("Exportar...", "button")
        return self
