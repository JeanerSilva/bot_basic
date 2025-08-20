#!/usr/bin/env python3
"""
PBI Bot - Aplicação principal
Arquitetura refatorada com separação de responsabilidades
"""

import sys
from core import DriverManager, ElementManager, WebActions
from flow import testa_flow


class PbiBot:
    """Classe principal que orquestra a aplicação"""
    
    def __init__(self):
        self.driver_manager = DriverManager()
        self.element_manager = ElementManager()
        self.web_actions = None
    
    def inicializar(self):
        """Inicializa o driver e as ações web"""
        print("🚀 Inicializando PBI Bot...")
        
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
    
    def executar_teste(self):
        """Executa o fluxo de teste"""
        if not self.web_actions:
            raise RuntimeError("WebActions não foi inicializado. Execute inicializar() primeiro.")
        
        print("🧪 Executando fluxo de teste...")
        testa_flow(self.web_actions, teste=True)
    
    def encerrar(self):
        """Encerra a aplicação"""
        print("🛑 Encerrando PBI Bot...")
        self.driver_manager.shutdown()
        print("✅ PBI Bot encerrado com sucesso!")
    
    def executar(self):
        """Executa o fluxo principal da aplicação"""
        try:
            self.inicializar()
            self.executar_teste()
            if self.web_actions:
                self.web_actions.wait_for_dom(timeout=1)
        finally:
            self.encerrar()


def main():
    """Função principal"""
    # Verifica se deve executar automaticamente
    if len(sys.argv) > 1 and sys.argv[1].lower() == '/y':
        print("Iniciando automaticamente...")
        bot = PbiBot()
        bot.executar()
    else:
        # Solicita confirmação do usuário
        resposta = input("\n⚠️ Você precisa estar previamente logado no SIOP.\n\n"
                        "O navegador Microsoft Edge será fechado. Deseja continuar? (s/n): ").strip().lower()
        
        if resposta != 's':
            print("Operação cancelada pelo usuário.")
            return
        
        bot = PbiBot()
        bot.executar()


if __name__ == "__main__":
    main()
