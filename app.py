#!/usr/bin/env python3
"""
PBI Bot - Aplicação Principal
Arquitetura limpa e moderna
"""

import sys
from pathlib import Path
from core import DriverManager, ElementManager, WebActions
from flows import TestFlow


class PbiBot:
    """Aplicação principal do PBI Bot"""
    
    def __init__(self):
        self.driver_manager = DriverManager()
        self.element_manager = ElementManager()
        self.web_actions = None
    
    def initialize(self):
        """Inicializa a aplicação"""
        print("🚀 Inicializando PBI Bot...")
        
        try:
            # Limpa processos existentes
            self.driver_manager.cleanup_processes()
            
            # Inicia o driver
            driver, wait = self.driver_manager.start_driver()
            
            # Cria WebActions
            self.web_actions = WebActions(
                driver=driver,
                wait=wait,
                actions=self.driver_manager.get_actions(),
                element_manager=self.element_manager
            )
            
            print("✅ PBI Bot inicializado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar: {e}")
            return False
    
    def run_test_flow(self):
        """Executa o fluxo de teste"""
        if not self.web_actions:
            raise RuntimeError("WebActions não foi inicializado")
        
        print("🧪 Executando fluxo de teste...")
        test_flow = TestFlow(self.web_actions)
        return test_flow.execute()
    
    def shutdown(self):
        """Encerra a aplicação"""
        print("🛑 Encerrando PBI Bot...")
        if self.driver_manager:
            self.driver_manager.shutdown()
        print("✅ PBI Bot encerrado com sucesso!")
    
    def run(self):
        """Executa a aplicação completa"""
        try:
            if not self.initialize():
                return False
            
            # Executa o fluxo principal
            success = self.run_test_flow()
            
            if success:
                print("🎉 Fluxo executado com sucesso!")
                self.web_actions.wait(2)
            else:
                print("💥 Fluxo falhou!")
            
            return success
            
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            return False
        finally:
            self.shutdown()


def main():
    """Função principal"""
    print("🤖 PBI Bot - Versão Limpa")
    print("=" * 40)
    
    # Verifica argumentos
    auto_mode = len(sys.argv) > 1 and sys.argv[1].lower() == '/y'
    
    if auto_mode:
        print("🚀 Modo automático ativado")
        bot = PbiBot()
        success = bot.run()
        sys.exit(0 if success else 1)
    else:
        # Modo interativo
        print("⚠️ Você precisa estar previamente logado no SIOP.")
        print("O navegador Microsoft Edge será fechado.")
        
        response = input("\nDeseja continuar? (s/n): ").strip().lower()
        
        if response == 's':
            bot = PbiBot()
            success = bot.run()
            sys.exit(0 if success else 1)
        else:
            print("Operação cancelada pelo usuário.")


if __name__ == "__main__":
    main()
