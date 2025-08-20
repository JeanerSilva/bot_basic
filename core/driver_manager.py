import subprocess
import time
import os
import re
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import SessionNotCreatedException
from config import config


class DriverManager:
    """Gerencia o driver do navegador Edge"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.actions = None
    
    def cleanup_processes(self):
        """Limpa processos do Edge existentes"""
        print("🧹 Limpando processos do Edge...")
        try:
            # Para processos do Edge
            subprocess.run(["taskkill", "/f", "/im", "msedge.exe"], 
                         check=False, capture_output=True)
            
            # Para processos do EdgeDriver
            subprocess.run(["taskkill", "/f", "/im", "msedgedriver.exe"], 
                         check=False, capture_output=True)
            
            time.sleep(2)  # Aguarda os processos terminarem
            print("✅ Processos limpos com sucesso!")
            
        except Exception as e:
            print(f"⚠️ Erro ao limpar processos: {e}")
    
    def start_driver(self, max_attempts=3, delay=5):
        """Inicia o driver do Edge"""
        print("🚀 Iniciando driver do Edge...")
        
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"📋 Tentativa {attempt}/{max_attempts}")
                
                # Cria opções do Edge
                edge_options = self._create_edge_options()
                
                # Cria serviço
                service = self._create_edge_service()
                
                # Inicia o driver
                self.driver = webdriver.Edge(service=service, options=edge_options)
                self.wait = WebDriverWait(self.driver, 120)
                self.actions = ActionChains(self.driver)
                
                print("✅ Driver iniciado com sucesso!")
                return self.driver, self.wait
                
            except SessionNotCreatedException as e:
                print(f"❌ Erro na tentativa {attempt}: {e}")
                if attempt < max_attempts:
                    print(f"⏳ Aguardando {delay} segundos...")
                    time.sleep(delay)
                else:
                    raise RuntimeError(f"Falha ao iniciar driver após {max_attempts} tentativas")
    
    def _create_edge_options(self):
        """Cria as opções do Edge"""
        options = Options()
        
        # Configurações de estabilidade
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        
        # Configurações de perfil
        try:
            profile_path = os.path.expandvars(config.EDGE_DIR)
            profile_path_clean = re.sub(r'\\+', r'\\\\', profile_path)
            
            options.add_argument(f'--user-data-dir={profile_path_clean}')
            options.add_argument(f'--profile-directory={config.PERFIL_EDGE_PADRAO}')
            print(f"✅ Perfil configurado: {profile_path_clean}")
            
        except Exception as e:
            print(f"⚠️ Erro ao configurar perfil: {e}")
            # Fallback para modo incognito
            options.add_argument("--incognito")
            options.add_argument("--disable-user-data-dir")
            print("⚠️ Usando modo incognito")
        
        return options
    
    def _create_edge_service(self):
        """Cria o serviço do Edge"""
        return Service(
            executable_path=str(config.DRIVER_DIR),
            log_path="logs/edge_driver.log",
            service_args=["--verbose"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    
    def get_driver(self):
        """Retorna o driver atual"""
        return self.driver
    
    def get_wait(self):
        """Retorna o WebDriverWait atual"""
        return self.wait
    
    def get_actions(self):
        """Retorna o ActionChains atual"""
        return self.actions
    
    def shutdown(self):
        """Encerra o driver"""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Driver encerrado com sucesso!")
            except Exception as e:
                print(f"⚠️ Erro ao encerrar driver: {e}")
            finally:
                self.driver = None
                self.wait = None
                self.actions = None
