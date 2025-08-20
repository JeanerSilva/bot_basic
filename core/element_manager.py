import json
import os
from config import config


class ElementManager:
    """Gerencia o carregamento e acesso aos elementos definidos no JSON"""
    
    def __init__(self):
        self._elementos = None
        self._urls = None
        self._load_elements()
        self._load_urls()
    
    def _load_elements(self):
        """Carrega os elementos do arquivo JSON"""
        try:
            with open(os.path.join(config.BASE_DIR, "config/elementos.json"), "r", encoding="utf-8") as f:
                self._elementos = json.load(f)
        except Exception as e:
            print(f"❌ Erro ao carregar elementos.json: {e}")
            self._elementos = []
    
    def _load_urls(self):
        """Carrega as URLs do arquivo JSON"""
        try:
            with open(os.path.join(config.BASE_DIR, "config/urls.json"), "r", encoding="utf-8") as f:
                self._urls = json.load(f)
        except Exception as e:
            print(f"❌ Erro ao carregar urls.json: {e}")
            self._urls = []
    
    def get_xpath_elemento(self, elemento):
        """Retorna o xpath de um elemento específico"""
        tipo = "xpath"
        for elem in self._elementos:
            if elem["item"] == elemento:
                return elem.get(tipo)
        raise ValueError(f"Elemento '{elemento}' com tipo '{tipo}' não encontrado.")
    
    def get_xpath_elemento_parametrizado(self, nome_item, **kwargs):
        """Retorna o xpath de um elemento com parâmetros substituídos"""
        for elem in self._elementos:
            if elem["item"] == nome_item:
                xpath_template = elem.get("xpath")
                if not xpath_template:
                    raise ValueError(f"Elemento '{nome_item}' não tem xpath definido.")
                for key, value in kwargs.items():
                    xpath_template = xpath_template.replace(f"${{{key}}}", str(value))
                return xpath_template
        raise ValueError(f"Elemento '{nome_item}' não encontrado.")
    
    def get_url(self, atividade):
        """Retorna a URL para uma atividade específica"""
        for item in self._urls:
            if item["atividade"] == atividade:
                return item["url"]
        raise ValueError(f"URL para atividade '{atividade}' não encontrada.")
    
    def reload(self):
        """Recarrega os arquivos de configuração"""
        self._load_elements()
        self._load_urls()
