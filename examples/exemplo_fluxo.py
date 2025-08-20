#!/usr/bin/env python3
"""
Exemplo de como criar um novo fluxo usando a nova arquitetura
"""

from core import WebActions


class ExemploFluxo:
    """Exemplo de fluxo de negócio"""
    
    def __init__(self, web_actions: WebActions, parametro1: str, parametro2: int):
        self.web_actions = web_actions
        self.parametro1 = parametro1
        self.parametro2 = parametro2
    
    def executar(self):
        """Executa o fluxo completo"""
        print(f"🚀 Executando fluxo com parâmetros: {self.parametro1}, {self.parametro2}")
        
        try:
            # 1. Acessar a página inicial
            self.web_actions.acessa("pagina_inicial")
            
            # 2. Aguardar carregamento
            self.web_actions.espera(2)
            
            # 3. Navegar para o painel
            self.web_actions.navega_para_painel()
            
            # 4. Preencher formulário
            self.web_actions.preenche_input("Nome do Campo", "campo_nome", self.parametro1)
            self.web_actions.preenche_input("Valor", "campo_valor", str(self.parametro2))
            
            # 5. Selecionar opção
            self.web_actions.preenche_seletor("Tipo", "//select[@id='tipo']", "Opção A")
            
            # 6. Clicar botão
            self.web_actions.clica_botao_tipo("Salvar", "submit")
            
            # 7. Aguardar processamento
            self.web_actions.espera(3)
            
            print("✅ Fluxo executado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro durante execução do fluxo: {e}")
            return False
    
    def validar_resultado(self):
        """Valida se o resultado foi o esperado"""
        try:
            # Aqui você pode implementar validações específicas
            elemento_resultado = self.web_actions.aguarda_elemento(
                "Mensagem de sucesso", 
                "//div[@class='success-message']"
            )
            
            if elemento_resultado:
                texto = elemento_resultado.text
                print(f"✅ Resultado validado: {texto}")
                return True
            else:
                print("❌ Resultado não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro na validação: {e}")
            return False


def exemplo_fluxo(web_actions: WebActions, parametro1: str = "padrão", parametro2: int = 0):
    """Factory function para criar e executar o fluxo de exemplo"""
    fluxo = ExemploFluxo(web_actions, parametro1, parametro2)
    
    # Executa o fluxo
    sucesso = fluxo.executar()
    
    if sucesso:
        # Valida o resultado
        fluxo.validar_resultado()
    
    return fluxo


# Exemplo de uso:
if __name__ == "__main__":
    print("Este arquivo é um exemplo de como criar fluxos.")
    print("Para usar, importe a função 'exemplo_fluxo' em seu código principal.")
