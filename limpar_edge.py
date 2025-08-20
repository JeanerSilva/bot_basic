#!/usr/bin/env python3
"""
Script para limpar completamente o Microsoft Edge
"""

import os
import subprocess
import time
import shutil
from pathlib import Path


def limpar_processos():
    """Para todos os processos relacionados ao Edge"""
    print("🧹 Parando processos do Edge...")
    
    processos = ["msedge.exe", "msedgedriver.exe"]
    
    for processo in processos:
        try:
            result = subprocess.run(["taskkill", "/f", "/im", processo], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {processo} encerrado")
            else:
                print(f"⚠️ {processo} não estava rodando")
        except Exception as e:
            print(f"⚠️ Erro ao encerrar {processo}: {e}")
    
    # Aguarda um pouco para os processos terminarem
    time.sleep(3)


def limpar_arquivos_lock():
    """Remove arquivos de lock do perfil do Edge"""
    print("\n🔓 Removendo arquivos de lock...")
    
    try:
        from config import config
        
        perfil_path = os.path.expandvars(config.EDGE_DIR)
        perfil_completo = os.path.join(perfil_path, config.PERFIL_EDGE_PADRAO)
        
        if os.path.exists(perfil_completo):
            print(f"📁 Verificando perfil: {perfil_completo}")
            
            # Lista arquivos que podem ser locks
            lock_patterns = ["lock", "lockfile", "singleton", "lockfile"]
            
            for arquivo in os.listdir(perfil_completo):
                if any(pattern in arquivo.lower() for pattern in lock_patterns):
                    arquivo_path = os.path.join(perfil_completo, arquivo)
                    try:
                        os.remove(arquivo_path)
                        print(f"✅ Removido: {arquivo}")
                    except Exception as e:
                        print(f"⚠️ Não foi possível remover {arquivo}: {e}")
            else:
                print("✅ Nenhum arquivo de lock encontrado")
        else:
            print(f"⚠️ Perfil não encontrado: {perfil_completo}")
            
    except Exception as e:
        print(f"⚠️ Erro ao limpar arquivos de lock: {e}")


def limpar_cache_edge():
    """Limpa cache e dados temporários do Edge"""
    print("\n🗑️ Limpando cache do Edge...")
    
    try:
        from config import config
        
        perfil_path = os.path.expandvars(config.EDGE_DIR)
        cache_dirs = ["Cache", "Code Cache", "GPUCache", "Service Worker"]
        
        for cache_dir in cache_dirs:
            cache_path = os.path.join(perfil_path, cache_dir)
            if os.path.exists(cache_path):
                try:
                    shutil.rmtree(cache_path)
                    print(f"✅ Cache removido: {cache_dir}")
                except Exception as e:
                    print(f"⚠️ Erro ao remover {cache_dir}: {e}")
            else:
                print(f"⚠️ Diretório de cache não encontrado: {cache_dir}")
                
    except Exception as e:
        print(f"⚠️ Erro ao limpar cache: {e}")


def reiniciar_servicos():
    """Reinicia serviços relacionados ao Edge"""
    print("\n🔄 Reiniciando serviços...")
    
    servicos = ["BITS", "wuauserv"]  # Serviços que podem afetar o Edge
    
    for servico in servicos:
        try:
            # Para o serviço
            subprocess.run(["net", "stop", servico], 
                         capture_output=True, text=True, timeout=10)
            time.sleep(2)
            
            # Inicia o serviço
            subprocess.run(["net", "start", servico], 
                         capture_output=True, text=True, timeout=10)
            print(f"✅ Serviço {servico} reiniciado")
            
        except Exception as e:
            print(f"⚠️ Erro ao reiniciar {servico}: {e}")


def verificar_limpeza():
    """Verifica se a limpeza foi bem-sucedida"""
    print("\n🔍 Verificando resultado da limpeza...")
    
    try:
        # Verifica se ainda há processos
        result = subprocess.run(["tasklist", "/fi", "imagename eq msedge.exe"], 
                              capture_output=True, text=True, timeout=10)
        
        if "msedge.exe" in result.stdout:
            print("❌ Ainda há processos do Edge rodando")
            return False
        else:
            print("✅ Nenhum processo do Edge em execução")
            return True
            
    except Exception as e:
        print(f"⚠️ Erro ao verificar: {e}")
        return False


def main():
    """Função principal"""
    print("🧹 LIMPEZA COMPLETA DO MICROSOFT EDGE")
    print("=" * 50)
    
    print("⚠️ ATENÇÃO: Este script irá:")
    print("   - Parar todos os processos do Edge")
    print("   - Remover arquivos de lock")
    print("   - Limpar cache")
    print("   - Reiniciar serviços relacionados")
    
    resposta = input("\nDeseja continuar? (s/n): ").strip().lower()
    if resposta != 's':
        print("Operação cancelada.")
        return
    
    # Executa a limpeza
    limpar_processos()
    limpar_arquivos_lock()
    limpar_cache_edge()
    reiniciar_servicos()
    
    # Verifica o resultado
    if verificar_limpeza():
        print("\n🎉 Limpeza concluída com sucesso!")
        print("💡 Agora tente executar a aplicação novamente.")
    else:
        print("\n⚠️ Limpeza parcial. Considere reiniciar o computador.")


if __name__ == "__main__":
    main()
