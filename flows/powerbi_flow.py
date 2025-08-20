from core import WebActions
from selenium.webdriver.common.by import By
import re


class PowerBIFlow:
    """Classe responsável por executar o fluxo de leitura do Power BI"""
    
    def __init__(self, web_actions: WebActions):
        self.web_actions = web_actions

    def executar(self):    
        print("🚀 Iniciando fluxo de leitura do Power BI...")
        
        # URL do Power BI
        powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiODhhNmNhZjctZjYxNS00ZjNmLWJlNmUtYTEwZjcyYTJiMGJjIiwidCI6IjNlYzkyOTY5LTVhNTEtNGYxOC04YWM5LWVmOThmYmFmYTk3OCJ9"
        
        try:
            # Navega para o Power BI
            print(f"🌐 Navegando para: {powerbi_url}")
            self.web_actions.driver.get(powerbi_url)
            
            # Aguarda o carregamento da página
            print("⏳ Aguardando carregamento da página...")
            self.web_actions.wait_for_dom(timeout=20)
            
                        # Aguarda mais tempo para garantir que o Power BI carregue completamente
            print("⏳ Aguardando renderização do Power BI...")
            self.web_actions.wait_for_jquery(timeout=15)
            
            # Aguarda especificamente por elementos do Power BI
            self._wait_for_powerbi_elements()

                        # Debug: lista todos os elementos numéricos encontrados
            self._debug_elementos_numericos()

            # Tenta localizar o elemento visual usando diferentes estratégias
            valor = self._ler_valor_objetivos()

            if valor:
                print(f"✅ Valor lido com sucesso: {valor}")
                return valor
            else:
                print("❌ Não foi possível ler o valor dos Objetivos Específicos")
                return None
                
        except Exception as e:
            print(f"❌ Erro durante a execução do fluxo: {e}")
            # Tira screenshot em caso de erro
            self.web_actions.take_screenshot("powerbi_error.png")
            return None
    
    def _wait_for_powerbi_elements(self):
        """Aguarda elementos específicos do Power BI estarem prontos"""
        print("🔍 Aguardando elementos do Power BI...")
        
        max_tentativas = 30  # 30 tentativas = ~15 segundos máximo
        tentativa = 0
        
        while tentativa < max_tentativas:
            # Verifica elementos estruturais do Power BI
            elementos_estruturais = self._count_powerbi_structural_elements()
            
            # Verifica se existem elementos com conteúdo numérico
            elementos_com_numeros = self._count_elements_with_numbers()
            
            if elementos_estruturais > 3 and elementos_com_numeros > 0:
                print(f"✅ Power BI carregado! {elementos_estruturais} elementos estruturais e {elementos_com_numeros} com números")
                return True
            
            tentativa += 1
            # Usa verificação do DOM que adiciona latência natural
            for _ in range(5):  # ~500ms total
                self.web_actions.driver.execute_script("return document.readyState;")
        
        print("⚠️ Timeout aguardando elementos do Power BI")
        return False
    
    def _count_powerbi_structural_elements(self):
        """Conta elementos estruturais do Power BI"""
        elementos_powerbi = [
            "//svg",                                    # SVGs são comuns em visuals do Power BI
            "//*[contains(@class, 'visual')]",         # Elementos com classe visual
            "//*[contains(@class, 'card')]",           # Cards visuais
            "//*[@data-automation-type='visual']",     # Elementos com automation-type
        ]
        
        total = 0
        for xpath in elementos_powerbi:
            try:
                elements = self.web_actions.driver.find_elements(By.XPATH, xpath)
                total += len(elements)
            except:
                continue
        return total
    
    def _count_elements_with_numbers(self):
        """Conta elementos que contêm números"""
        xpaths_numericos = [
            "//*[contains(@class, 'value')]",
            "//*[text() and string-length(text()) <= 4 and translate(text(), '0123456789', '') = '']",
            "//text[string-length(.) <= 4 and translate(., '0123456789', '') = '']",
        ]
        
        total = 0
        for xpath in xpaths_numericos:
            try:
                elements = self.web_actions.driver.find_elements(By.XPATH, xpath)
                total += len(elements)
            except:
                continue
        return total

    def _debug_elementos_numericos(self):
        """Debug: mostra todos os elementos numéricos encontrados"""
        print("🔍 Debug: Listando elementos numéricos encontrados...")
        
        xpaths_debug = [
            "//*[contains(@class, 'value')]",
            "//*[text() and string-length(text()) <= 4]",
            "//text[string-length(.) <= 4]",
            "//*[contains(text(), '463')]",
            "//*[contains(text(), 'Objetivos')]"
        ]
        
        for i, xpath in enumerate(xpaths_debug, 1):
            try:
                elements = self.web_actions.driver.find_elements(By.XPATH, xpath)
                print(f"   {i}. XPath: {xpath[:50]}... → {len(elements)} elementos")
                
                for j, element in enumerate(elements[:3]):  # Mostra apenas os 3 primeiros
                    try:
                        texto = element.text.strip()
                        if texto:
                            print(f"      [{j+1}] Texto: '{texto}' (Tag: {element.tag_name})")
                        else:
                            print(f"      [{j+1}] Texto vazio (Tag: {element.tag_name})")
                    except Exception as e:
                        print(f"      [{j+1}] Erro ao ler texto: {e}")
                        
                if len(elements) > 3:
                    print(f"      ... e mais {len(elements) - 3} elementos")
                    
            except Exception as e:
                print(f"   {i}. Erro no XPath: {str(e)[:50]}...")

    def _ler_valor_objetivos(self):
        """Tenta ler o valor dos Objetivos Específicos usando diferentes estratégias"""
        
        # Estratégia 1: Buscar pelo texto "Objetivos Específicos" usando diferentes XPaths
        try:
            print("🔍 Tentativa 1: Buscando por 'Objetivos Específicos'...")
            
            xpaths_objetivos = [
                "//text[contains(text(), 'Objetivos Específicos')]",
                "//*[contains(text(), 'Objetivos Específicos')]",
                "//div[contains(text(), 'Objetivos Específicos')]",
                "//span[contains(text(), 'Objetivos Específicos')]",
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'objetivos específicos')]",
                "//*[contains(translate(text(), 'ÁÉÍÓÚÀÈÌÒÙÃÕÂÊÎÔÛ', 'aeiouaeiouaoaeiou'), 'objetivos especificos')]"
            ]
            
            elemento_objetivos = None
            for xpath in xpaths_objetivos:
                try:
                    elemento_objetivos = self.web_actions.driver.find_element(By.XPATH, xpath)
                    if elemento_objetivos:
                        print(f"✅ Texto encontrado com XPath: {xpath}")
                        break
                except:
                    continue
            
            if elemento_objetivos:
                valor = self._buscar_valor_proximo(elemento_objetivos)
                if valor:
                    return valor
                    
        except Exception as e:
            print(f"⚠️ Estratégia 1 falhou: {e}")
        
        # Estratégia 2: Buscar por elementos com classe "value" que contenham números
        try:
            print("🔍 Tentativa 2: Buscando por elementos com classe 'value'...")
            
            elementos_valor = self.web_actions.driver.find_elements(
                By.XPATH, 
                "//*[@class='value']"
            )
            
            for elemento in elementos_valor:
                texto = elemento.text.strip()
                if texto.isdigit():
                    print(f"📊 Valor encontrado: {texto}")
                    return texto
                    
        except Exception as e:
            print(f"⚠️ Estratégia 2 falhou: {e}")
        
        # Estratégia 3: Buscar por qualquer texto que seja apenas números
        try:
            print("🔍 Tentativa 3: Buscando por textos numéricos...")
            
            elementos_texto = self.web_actions.driver.find_elements(
                By.XPATH, 
                "//*[text() and string-length(text()) <= 4]"
            )
            
            for elemento in elementos_texto:
                texto = elemento.text.strip()
                if texto.isdigit() and len(texto) <= 4:  # Limita a números de até 4 dígitos
                    print(f"📊 Valor numérico encontrado: {texto}")
                    return texto
                    
        except Exception as e:
            print(f"⚠️ Estratégia 3 falhou: {e}")
        
        # Estratégia 4: Buscar por SVG com texto específico
        try:
            print("🔍 Tentativa 4: Buscando por SVG com 'Objetivos Específicos'...")
            
            svg_element = self.web_actions.driver.find_element(
                By.XPATH, 
                "//svg[.//*[contains(text(), 'Objetivos Específicos')]]"
            )
            
            if svg_element:
                # Busca o valor dentro do SVG
                valor_element = svg_element.find_element(
                    By.XPATH, 
                    ".//*[@class='value']"
                )
                
                if valor_element:
                    valor = valor_element.text.strip()
                    if valor.isdigit():
                        return valor
                        
        except Exception as e:
            print(f"⚠️ Estratégia 4 falhou: {e}")
        
        # Estratégia 5: Buscar por qualquer elemento que contenha "463"
        try:
            print("🔍 Tentativa 5: Buscando por elementos que contenham '463'...")
            
            elementos_463 = self.web_actions.driver.find_elements(
                By.XPATH, 
                "//*[contains(text(), '463')]"
            )
            
            print(f"   Encontrados {len(elementos_463)} elementos com '463'")
            
            for i, elemento in enumerate(elementos_463):
                try:
                    texto = elemento.text.strip()
                    print(f"   Elemento {i+1}: '{texto}' (Tag: {elemento.tag_name})")
                    
                    if '463' in texto:
                        # Se o texto é exatamente "463", retorna
                        if texto == '463':
                            print(f"✅ Valor exato encontrado: {texto}")
                            return texto
                        
                        # Se contém 463, tenta extrair números
                        matches = re.findall(r'\b\d+\b', texto)
                        for match in matches:
                            if match == '463':
                                print(f"✅ Valor extraído: {match}")
                                return match
                                
                except Exception as e:
                    print(f"   Erro ao processar elemento {i+1}: {e}")
                        
        except Exception as e:
            print(f"⚠️ Estratégia 5 falhou: {e}")
        
        return None

    def _buscar_valor_proximo(self, elemento_objetivos):
        """Busca o valor numérico próximo ao elemento de objetivos"""
        try:
            # Tenta encontrar o valor no elemento pai
            container = elemento_objetivos.find_element(By.XPATH, "./..")
            
            # Busca por elementos com classe 'value'
            elementos_valor = container.find_elements(By.XPATH, ".//*[@class='value']")
            for elemento in elementos_valor:
                valor = elemento.text.strip()
                if valor.isdigit():
                    return valor
            
            # Busca por elementos de texto que sejam números
            elementos_texto = container.find_elements(By.XPATH, ".//text")
            for elemento in elementos_texto:
                valor = elemento.text.strip()
                if valor.isdigit() and len(valor) <= 4:
                    return valor
            
            # Busca por elementos irmãos
            try:
                valor_element = elemento_objetivos.find_element(By.XPATH, "./preceding-sibling::*[1]")
                if valor_element:
                    valor = valor_element.text.strip()
                    if valor.isdigit():
                        return valor
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Erro ao buscar valor próximo: {e}")
        
        return None


def powerbi_flow(web_actions: WebActions):
    """Factory function para criar e executar o fluxo do Power BI"""
    return PowerBIFlow(web_actions).executar()
