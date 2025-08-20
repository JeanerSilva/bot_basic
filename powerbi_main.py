#!/usr/bin/env python3
"""
PBI Bot - Fluxo específico para leitura do Power BI
"""

import sys
from core import DriverManager, ElementManager, WebActions
from flows import powerbi_flow


class PowerBIBot:
    """Classe específica para executar o fluxo do Power BI"""
    
    def __init__(self):
        self.driver_manager = DriverManager()
        self.element_manager = ElementManager()
        self.web_actions = None
    
    def inicializar(self):
        """Inicializa o driver e as ações web"""
        print("🚀 Inicializando PBI Bot para Power BI...")
        
        # Finaliza navegadores existentes
        self.driver_manager.cleanup_processes()
        
        # Inicia o driver
        driver, wait = self.driver_manager.start_driver()
        
        # Cria as ações web
        self.web_actions = WebActions(
            driver=driver,
            wait=wait,
            actions=self.driver_manager.get_actions(),
            element_manager=self.element_manager
        )
        
        print("✅ PBI Bot inicializado com sucesso!")
    
    def executar_powerbi_flow(self):
        """Executa o fluxo específico do Power BI"""
        if not self.web_actions:
            raise RuntimeError("WebActions não foi inicializado. Execute inicializar() primeiro.")
        
        print("📊 Executando fluxo de leitura do Power BI...")
        valor = powerbi_flow(self.web_actions)
        
        if valor:
            print(f"\n🎯 RESULTADO: O valor dos Objetivos Específicos é: {valor}")
            return valor
        else:
            print("\n❌ Não foi possível obter o valor dos Objetivos Específicos")
            return None
    
    def encerrar(self):
        """Encerra a aplicação"""
        print("🛑 Encerrando PBI Bot...")
        self.driver_manager.shutdown()
        print("✅ PBI Bot encerrado com sucesso!")
    
    def executar(self):
        """Executa o fluxo principal da aplicação"""
        try:
            self.inicializar()
            resultado = self.executar_powerbi_flow()
            
            if resultado:
                print(f"\n✅ Fluxo executado com sucesso! Valor lido: {resultado}")
            else:
                print("\n❌ Fluxo falhou ao ler o valor")
            
            # Aguarda um pouco antes de encerrar
            if self.web_actions:
                self.web_actions.wait_for_dom(timeout=3)
            
        except Exception as e:
            print(f"❌ Erro durante a execução: {e}")
            # Tira screenshot em caso de erro
            if self.web_actions:
                self.web_actions.take_screenshot("powerbi_error_main.png")
        finally:
            self.encerrar()


def main():
    """Função principal"""
    print("=" * 60)
    print("🔍 PBI BOT - LEITOR DE POWER BI")
    print("=" * 60)
    print("Este bot irá:")
    print("1. Abrir o Power BI no navegador")
    print("2. Ler o valor dos 'Objetivos Específicos'")
    print("3. Exibir o resultado")
    print("=" * 60)
    
    # Verifica se deve executar automaticamente
    if len(sys.argv) > 1 and sys.argv[1].lower() == '/y':
        print("Iniciando automaticamente...")
        bot = PowerBIBot()
        bot.executar()
    else:
        # Solicita confirmação do usuário
        resposta = input("\n⚠️ O navegador Microsoft Edge será fechado. Deseja continuar? (s/n): ").strip().lower()
        
        if resposta != 's':
            print("Operação cancelada pelo usuário.")
            return
        
        bot = PowerBIBot()
        bot.executar()


if __name__ == "__main__":
    main()
