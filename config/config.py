from pathlib import Path
#URL_BASE = "https://www.siop.planejamento.gov.br"
URL_BASE = "https://app.powerbi.com/view?r=eyJrIjoiODhhNmNhZjctZjYxNS00ZjNmLWJlNmUtYTEwZjcyYTJiMGJjIiwidCI6IjNlYzkyOTY5LTVhNTEtNGYxOC04YWM5LWVmOThmYmFmYTk3OCJ9"

# Configurações do Edge
PERFIL_EDGE_PADRAO = "Default"
EDGE_DIR = r'%LOCALAPPDATA%\\Microsoft\\Edge\\User Data'

# Configurações alternativas para resolver problemas
USAR_PERFIL_TEMPORARIO = False  # Mude para True se houver problemas de perfil
USAR_MODO_INCOGNITO = False     # Mude para True se houver problemas de perfil

# Diretórios
BASE_DIR = BASE_DIR = Path(__file__).resolve().parent.parent
DRIVER_DIR = BASE_DIR / "drivers" / "edge" / "msedgedriver.exe"

# Configurações gerais
JQUERY = True
