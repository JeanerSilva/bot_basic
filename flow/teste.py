from core import WebActions


class TesteFlow:
    """Classe responsável por executar o fluxo de teste"""
    
    def __init__(self, web_actions: WebActions, teste: bool = False):
        if not teste:
            raise ValueError("❌ Parâmetro 'teste' é obrigatório e não pode estar vazio.")
        self.teste = teste
        self.web_actions = web_actions

    def executar(self):    
        print("Executando teste...")
        # Aqui você pode implementar a lógica específica do teste
        # usando self.web_actions para todas as operações web
        return self


def testa_flow(web_actions: WebActions, teste: bool = True):
    """Factory function para criar e executar o fluxo de teste"""
    return TesteFlow(web_actions, teste).executar()


