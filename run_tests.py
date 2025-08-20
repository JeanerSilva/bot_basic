#!/usr/bin/env python3
"""
Script para executar testes da aplicação
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"\n{'='*50}")
    print(f"🚀 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Comando executado com sucesso!")
        if result.stdout:
            print("📤 Saída:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar comando: {e}")
        if e.stdout:
            print("📤 Saída padrão:")
            print(e.stdout)
        if e.stderr:
            print("📤 Saída de erro:")
            print(e.stderr)
        return False


def main():
    """Função principal"""
    print("🧪 Executando testes da aplicação PBI Bot")
    
    # Verifica se pytest está instalado
    try:
        import pytest
        print("✅ pytest encontrado")
    except ImportError:
        print("❌ pytest não encontrado. Instalando...")
        run_command("pip install pytest pytest-mock pytest-cov", "Instalando dependências de teste")
    
    # Executa os testes
    success = run_command(
        "python -m pytest tests/ -v --cov=core --cov=flow --cov-report=term-missing",
        "Executando testes com cobertura"
    )
    
    if success:
        print("\n🎉 Todos os testes foram executados!")
    else:
        print("\n💥 Alguns testes falharam!")
        sys.exit(1)


if __name__ == "__main__":
    main()
