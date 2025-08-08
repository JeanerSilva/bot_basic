# objetivo_flow.py
import siop_utils as sb

class ObjetivoEspecificoFlow:
    def __init__(self, objetivo: str):
        if not objetivo or not str(objetivo).strip():
            raise ValueError("❌ Parâmetro 'objetivo' é obrigatório e não pode estar vazio.")
        self.objetivo = objetivo

    def acessar(self):
        sb.acessa("ppa->objetivo_específico")
        sb.seleciona_ano_e_perfil_e_muda_de_frame()
        return self

    def listar(self):
        sb.preenche_input("Objetivo Específico", "ppa.objetivo_especifico.objetivo_especifico_input", self.objetivo)
        sb.clica_botao_tipo("Procurar", "submit")
        return self

    def selecionar_primeiro(self):
        sb.clica_link("Seleciona primeiro objetivo", "tabela_resultados_objetivos_específicos.primeiro_item")
        return self

    def abrir_entregas(self):
        sb.clica_link("Botão Entregas", "objetivo_especifico.botao_entregas")
        return self

    def abrir_indicadores(self):
        sb.clica_link("Botão Indicadores", "objetivo_especifico.botao_indicadores")
        return self

    def acessar_indicador(self):
        sb.clica_link("Indicador do objetivo", "objetivo_especifico.botao_indicadores.indicador")
        return self

    def preencher_nota_do_usuario(self, nota):
        sb.preenche_input("Nota do usuário", "objetivo_especifico.informacoes_basicas.nota_do_usuario", nota)
        return self

    def clicar_link_entrega_por_texto(self, texto):
        sb.clica_link_por_texto_inicial(texto)
        return self
