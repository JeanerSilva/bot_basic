from pathlib import Path
URL_BASE = "https://www.siop.planejamento.gov.br"
#URL_BASE = "http://10.209.64.129"

PERFIL_PADRAO = "Controle de Qualidade - SEPLAN"
ANO_PADRAO = "2025"
PERFIL_EDGE_PADRAO = "Default"
EDGE_DIR = r'%LOCALAPPDATA%\\Microsoft\\Edge\\User Data'
BASE_DIR = BASE_DIR = Path(__file__).resolve().parent.parent
DRIVER_DIR = BASE_DIR / "drivers" / "edge" / "msedgedriver.exe"
JQUERY = True
