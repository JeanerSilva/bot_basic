import os
import re
from config import config

def listar_caminho():
    caminho = os.path.expandvars(config.EDGE_DIR)  
    caminho_ajustado = re.sub(r'\\+', r'\\\\', caminho) 
    argumento = f'--user-data-dir={caminho_ajustado}'    
    return argumento

def listar_perfis_edge():
    caminho_base = os.path.expandvars(config.EDGE_DIR)  
    perfis = []

    if os.path.exists(caminho_base):
        for item in os.listdir(caminho_base):
            caminho_completo = os.path.join(caminho_base, item)
            if os.path.isdir(caminho_completo) and (item == "Default" or item.startswith("Profile")):
                perfis.append(item)
    else:
        print("Caminho do Edge não encontrado.")

    return perfis

# Exemplo de uso
print(f"Caminho edge: {listar_caminho()}")

for perfil in listar_perfis_edge():
    print("Perfil encontrado:", perfil)
