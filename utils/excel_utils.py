import pandas as pd


class ExcelUtils:
    """Utilitários para manipulação de arquivos Excel"""
    
    @staticmethod
    def abrir_excel(arquivo, aba):
        """Abre um arquivo Excel e retorna uma aba específica"""
        try:
            return pd.read_excel(arquivo, sheet_name=aba)
        except Exception as e:
            print(f"❌ Erro ao abrir arquivo Excel '{arquivo}' na aba '{aba}': {e}")
            raise
    
    @staticmethod
    def salvar_excel(dataframe, arquivo, aba, index=False):
        """Salva um DataFrame em um arquivo Excel"""
        try:
            with pd.ExcelWriter(arquivo, engine='openpyxl', mode='a' if index else 'w') as writer:
                dataframe.to_excel(writer, sheet_name=aba, index=index)
            print(f"✅ Arquivo Excel salvo com sucesso: {arquivo}")
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo Excel '{arquivo}': {e}")
            raise
