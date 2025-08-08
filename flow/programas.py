# programa_flow.py
import siop_utils as sb

class ProgramaFlow:
    def __init__(self, codigo_programa: str):
        if not codigo_programa or not str(codigo_programa).strip():
            raise ValueError("❌ Parâmetro 'codigo_programa' é obrigatório e não pode estar vazio.")
        self.codigo_programa = codigo_programa

    def acessar(self):
        sb.acessa("ppa->programa")
        sb.seleciona_ano_e_perfil_e_muda_de_frame()
        return self

    def listar(self):
        sb.preenche_input("Programa", "ppa.programa.programa_input", self.codigo_programa)
        sb.clica_botao_tipo("Procurar", "submit")
        return self

    def limpar(self):
        sb.clica_botao_tipo("Limpar", "submit")
        return self

    def exportar(self):
        sb.aguarda_tabela("Tabela Programas", "tabela_resultados_programas")
        sb.clica_botao_tipo("Exportar...", "button")
        return self
