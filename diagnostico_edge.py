#!/usr/bin/env python3
"""
Script de diagnóstico para problemas com o Microsoft Edge
"""

import os
import subprocess
import sys
from pathlib import Path


def verificar_edge_instalado():
    """Verifica se o Edge está instalado"""
    print("🔍 Verificando instalação do Microsoft Edge...")
    
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    
    for path in edge_paths:
        if os.path.exists(path):
            print(f"✅ Edge encontrado em: {path}")
            return path
    
    print("❌ Edge não encontrado nos caminhos padrão")
    return None


def verificar_edge_driver():
    """Verifica se o EdgeDriver está disponível"""
    print("\n🔍 Verificando EdgeDriver...")
    
    driver_path = Path(__file__).parent / "drivers" / "edge" / "msedgedriver.exe"
    
    if driver_path.exists():
        print(f"✅ EdgeDriver encontrado em: {driver_path}")
        
        # Verifica versão
        try:
            result = subprocess.run([str(driver_path), "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"📋 Versão do EdgeDriver: {result.stdout.strip()}")
            else:
                print(f"⚠️ EdgeDriver retornou erro: {result.stderr}")
        except Exception as e:
            print(f"⚠️ Erro ao verificar versão: {e}")
        
        return driver_path
    else:
        print(f"❌ EdgeDriver não encontrado em: {driver_path}")
        return None


def verificar_processos_edge():
    """Verifica processos do Edge em execução"""
    print("\n🔍 Verificando processos do Edge...")
    
    try:
        # Verifica processos do Edge
        result = subprocess.run(["tasklist", "/fi", "imagename eq msedge.exe"], 
                              capture_output=True, text=True, timeout=10)
        
        if "msedge.exe" in result.stdout:
            print("⚠️ Processos do Edge em execução:")
            for line in result.stdout.split('\n'):
                if "msedge.exe" in line:
                    print(f"   {line.strip()}")
        else:
            print("✅ Nenhum processo do Edge em execução")
            
    except Exception as e:
        print(f"⚠️ Erro ao verificar processos: {e}")


def verificar_perfil_edge():
    """Verifica configuração do perfil do Edge"""
    print("\n🔍 Verificando perfil do Edge...")
    
    try:
        from config import config
        
        perfil_path = os.path.expandvars(config.EDGE_DIR)
        perfil_completo = os.path.join(perfil_path, config.PERFIL_EDGE_PADRAO)
        
        if os.path.exists(perfil_path):
            print(f"✅ Diretório de perfil encontrado: {perfil_path}")
            
            if os.path.exists(perfil_completo):
                print(f"✅ Perfil específico encontrado: {perfil_completo}")
                
                # Lista arquivos do perfil
                arquivos = os.listdir(perfil_completo)
                print(f"📁 Arquivos no perfil: {len(arquivos)}")
                
                # Verifica se há arquivos de lock
                lock_files = [f for f in arquivos if "lock" in f.lower() or "lockfile" in f.lower()]
                if lock_files:
                    print(f"⚠️ Arquivos de lock encontrados: {lock_files}")
                else:
                    print("✅ Nenhum arquivo de lock encontrado")
                    
            else:
                print(f"❌ Perfil específico não encontrado: {perfil_completo}")
        else:
            print(f"❌ Diretório de perfil não encontrado: {perfil_path}")
            
    except Exception as e:
        print(f"⚠️ Erro ao verificar perfil: {e}")


def limpar_processos_edge():
    """Tenta limpar processos do Edge"""
    print("\n🧹 Tentando limpar processos do Edge...")
    
    try:
        # Para processos do Edge
        result = subprocess.run(["taskkill", "/f", "/im", "msedge.exe"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Processos do Edge encerrados com sucesso")
        else:
            print(f"⚠️ Nenhum processo do Edge para encerrar: {result.stderr}")
            
        # Para processos do EdgeDriver
        result = subprocess.run(["taskkill", "/f", "/im", "msedgedriver.exe"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Processos do EdgeDriver encerrados com sucesso")
        else:
            print(f"⚠️ Nenhum processo do EdgeDriver para encerrar: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro ao limpar processos: {e}")


def testar_edge_manual():
    """Testa se o Edge pode ser iniciado manualmente"""
    print("\n🧪 Testando inicialização manual do Edge...")
    
    try:
        edge_path = verificar_edge_instalado()
        if not edge_path:
            print("❌ Não é possível testar sem o Edge instalado")
            return False
        
        # Tenta iniciar o Edge com argumentos básicos
        print("🚀 Iniciando Edge manualmente...")
        result = subprocess.run([edge_path, "--no-sandbox", "--disable-dev-shm-usage"], 
                              capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("✅ Edge iniciado manualmente com sucesso")
            return True
        else:
            print(f"⚠️ Edge retornou código: {result.returncode}")
            if result.stderr:
                print(f"📋 Erro: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✅ Edge iniciou (timeout - provavelmente funcionando)")
        return True
    except Exception as e:
        print(f"❌ Erro ao testar Edge manualmente: {e}")
        return False


def main():
    """Função principal"""
    print("🔧 DIAGNÓSTICO DO MICROSOFT EDGE")
    print("=" * 50)
    
    # Executa todas as verificações
    verificacoes = [
        ("Instalação do Edge", verificar_edge_instalado),
        ("EdgeDriver", verificar_edge_driver),
        ("Processos em Execução", verificar_processos_edge),
        ("Configuração do Perfil", verificar_perfil_edge),
        ("Teste Manual", testar_edge_manual)
    ]
    
    resultados = []
    for nome, verificacao in verificacoes:
        print(f"\n📋 {nome}")
        try:
            resultado = verificacao()
            resultados.append((nome, resultado is not None))
        except Exception as e:
            print(f"❌ Erro durante verificação: {e}")
            resultados.append((nome, False))
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO DE DIAGNÓSTICO")
    print("=" * 50)
    
    for nome, resultado in resultados:
        status = "✅ OK" if resultado else "❌ PROBLEMA"
        print(f"{nome}: {status}")
    
    # Recomendações
    print("\n💡 RECOMENDAÇÕES:")
    
    if not any(resultados):
        print("❌ Múltiplos problemas detectados. Considere:")
        print("   - Reinstalar o Microsoft Edge")
        print("   - Atualizar o EdgeDriver")
        print("   - Verificar permissões de usuário")
    elif resultados[0] and not resultados[1]:
        print("⚠️ Edge instalado mas EdgeDriver com problema:")
        print("   - Baixe a versão correta do EdgeDriver")
        print("   - Verifique se a versão é compatível com o Edge")
    elif resultados[0] and resultados[1] and not resultados[2]:
        print("⚠️ Edge e EdgeDriver OK, mas processos em conflito:")
        print("   - Execute o script de limpeza")
        print("   - Reinicie o computador se necessário")
    else:
        print("✅ Ambiente parece estar configurado corretamente")
        print("   - Tente executar a aplicação novamente")
        print("   - Se persistir, pode ser problema de perfil")


if __name__ == "__main__":
    main()
