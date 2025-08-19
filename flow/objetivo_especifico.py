import siop_utils as sb

class objetivo_especifico:
    def __init__(self, objetivo: str):
        if not objetivo or not str(objetivo).strip():
            raise ValueError("❌ Parâmetro 'objetivo' é obrigatório e não pode estar vazio.")
        self.objetivo = objetivo

    def acessa(self):
        sb.acessa("ppa->objetivo_específico")
        sb.seleciona_ano_e_perfil_e_muda_de_frame()
        return self

    def lista(self):
        sb.preenche_input("Objetivo Específico", "ppa.objetivo_especifico.objetivo_especifico_input", self.objetivo)
        sb.clica_botao_tipo("Procurar", "submit")
        return self

    def seleciona_objetivo_listado(self):
        sb.clica_link("Primeiro objetivo", "tabela_resultados_objetivos_específicos.primeiro_item", self.objetivo)
        return self

    def abre_entregas(self):
        sb.clica_link("Botão Entregas dentro do objetivo específico", "objetivo_especifico.botao_entregas")
        return self

    def abre_indicadores(self):
        sb.clica_link("Botão Indicadores", "objetivo_especifico.botao_indicadores")
        sb.clica_item_painel(
                "Painel de Indicadores",
                "objetivo_especifico.painel_indicadores",
                "Link do Indicador",
                "objetivo_especifico.botao_indicadores.indicador"
            )

        return self


    def acessa_indicador(self):
        sb.clica_link("Indicador do objetivo", "objetivo_especifico.botao_indicadores.indicador")
        return self

    def preenche_nota_do_usuario(self, nota):
        sb.preenche_input("Nota do usuário", "objetivo_especifico.informacoes_basicas.nota_do_usuario", nota)
        return self

    def clica_link_entrega_por_texto(self, texto):
        sb.clica_link_por_texto_inicial(texto)
        return self
    
    def apaga_arquivo_pac(self):
        sb.clica_link("Apaga arquivo", "objetivo-especifico.novopac.botao_excluir")
        sb.espera(1)
        sb.clica_botao_tipo("Confirmar", "submit")
        

    def adiciona_arquivo_pac(self, descricao, arquivo):
        sb.clica_botao_tipo("Adicionar...", "submit")
        sb.preenche_input("Descrição PAC", "objetivo-especifico.novopac.upload_file.input_descricao", descricao)
    
        iframe_locator = "//iframe[@title='Input File Frame' and contains(@class,'uploadFile')]"
        iframe = sb.aguarda_elemento("Iframe", iframe_locator)
        sb.driver.switch_to.frame(iframe)

        input_file = sb.aguarda_elemento("Input file", "//input[@type='file']")
        input_file.send_keys(arquivo)
        sb.clica_botao_tipo("Enviar", "submit")    

        sb.driver.switch_to.parent_frame()    
        
        pronto = "//div[contains(@class,'barraProgressoTxt')]"
        sb.aguarda_texto_no_elemento("Enviado", pronto, "xlsx")
        
        #sb.debug_contexto(sb)     
       
        sb.clica_botao_tipo("Confirmar", "submit")                                                              
        sb.clica_link_por_texto_inicial("Salvar")
        sb.driver.switch_to.default_content()
        sb.acessa("inicio")
        
