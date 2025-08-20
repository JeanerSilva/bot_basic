#!/usr/bin/env python3
"""
Exemplo de uso do fluxo do Power BI
"""

from core import DriverManager, ElementManager, WebActions
from flows import powerbi_flow


def exemplo_powerbi():
    """Exemplo de como usar o fluxo do Power BI"""
    
    # Inicializa o bot
    driver_manager = DriverManager()
    element_manager = ElementManager()
    
    try:
        print("🚀 Iniciando exemplo do Power BI...")
        
        # Inicia o driver
        driver, wait = driver_manager.start_driver()
        
        # Cria as ações web
        web_actions = WebActions(
            driver=driver,
            wait=wait,
            actions=driver_manager.get_actions(),
            element_manager=element_manager
        )
        
        print("✅ Bot inicializado!")
        
        # Executa o fluxo do Power BI
        valor = powerbi_flow(web_actions)
        
        if valor:
            print(f"\n🎯 Valor lido com sucesso: {valor}")
        else:
            print("\n❌ Falha ao ler o valor")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        
    finally:
        # Encerra o driver
        driver_manager.shutdown()
        print("✅ Driver encerrado")


if __name__ == "__main__":
    exemplo_powerbi()
