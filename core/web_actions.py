import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


class WebActions:
    """Ações web com Selenium"""
    
    def __init__(self, driver, wait, actions, element_manager):
        self.driver = driver
        self.wait = wait
        self.actions = actions
        self.element_manager = element_manager
        self.jquery_enabled = True
    
    # ============================================================================
    # NAVEGAÇÃO
    # ============================================================================
    
    def navigate_to(self, activity):
        """Navega para uma atividade específica"""
        from config import config
        url = self.element_manager.get_url(activity)
        full_url = config.URL_BASE + url
        self.driver.get(full_url)
        print(f"✅ Navegou para: {activity}")
    
    def navigate_to_panel(self):
        """Navega para o painel principal"""
        iframe = self.wait_for_element("Container principal", "//iframe")
        self.driver.switch_to.frame(iframe)
        print("✅ Entrou no painel principal")
    
    # ============================================================================
    # ELEMENTOS
    # ============================================================================
    
    def wait_for_element(self, description, xpath, timeout=None):
        """Aguarda um elemento aparecer"""
        if timeout is None:
            timeout = self.wait.timeout
        
        print(f"🕓 Aguardando: {description}")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            
            # Aguarda jQuery se habilitado
            if self.jquery_enabled:
                self.wait_for_jquery()
            
            print(f"✅ Elemento encontrado: {description}")
            return element
            
        except TimeoutException:
            self._handle_timeout_error(description, xpath)
            raise
    
    def wait_for_optional_element(self, description, xpath, timeout=3):
        """Aguarda um elemento opcional"""
        try:
            return self.wait_for_element(description, xpath, timeout)
        except TimeoutException:
            print(f"⚠️ Elemento opcional não encontrado: {description}")
            return None
    
    def wait_for_dom(self, timeout=10):
        """Aguarda o DOM ficar pronto"""
        print("🕓 Aguardando DOM...")
        
        for _ in range(timeout * 2):
            try:
                ready = self.driver.execute_script("return document.readyState === 'complete';")
                if ready:
                    print("✅ DOM pronto")
                    return
            except Exception:
                pass
            time.sleep(0.5)
        
        print("⚠️ DOM não ficou pronto")
    
    def wait_for_jquery(self, timeout=10):
        """Aguarda jQuery ficar inativo"""
        print("🕓 Aguardando jQuery...")
        
        for _ in range(timeout * 2):
            try:
                ready = self.driver.execute_script("""
                    return (
                        typeof jQuery === 'undefined' || 
                        (typeof jQuery.active !== 'undefined' && jQuery.active === 0)
                    );
                """)
                if ready:
                    print("✅ jQuery inativo")
                    return
            except Exception:
                pass
            time.sleep(0.5)
        
        print("⚠️ jQuery ainda ativo")
    
    # ============================================================================
    # INTERAÇÕES
    # ============================================================================
    
    def click(self, description, xpath):
        """Clica em um elemento"""
        element = self.wait_for_element(description, xpath)
        
        try:
            element.click()
            print(f"✅ Clicou em: {description}")
        except Exception:
            print(f"⚠️ Clique normal falhou, tentando JavaScript...")
            self.driver.execute_script("arguments[0].click();", element)
            print(f"✅ Clicou via JavaScript em: {description}")
    
    def click_button(self, text, button_type):
        """Clica em um botão específico"""
        xpath = f'//input[@type="{button_type}" and @value="{text}"]'
        self.click(f"Botão {text}", xpath)
    
    def click_link(self, description, element_name, number=0):
        """Clica em um link"""
        if number == 0:
            xpath = self.element_manager.get_xpath_elemento(element_name)
        else:
            xpath = self.element_manager.get_xpath_elemento_parametrizado(element_name, numero=number)
        
        self.click(description, xpath)
    
    def fill_input(self, description, element_name, text):
        """Preenche um campo de input"""
        xpath = self.element_manager.get_xpath_elemento(element_name)
        element = self.wait_for_element(description, xpath)
        
        try:
            element.clear()
            element.send_keys(text)
            print(f"✅ Preencheu {description}: {text}")
        except StaleElementReferenceException:
            print(f"⚠️ Elemento obsoleto, tentando novamente...")
            element = self.wait_for_element(description, xpath)
            element.clear()
            element.send_keys(text)
            print(f"✅ Preencheu {description}: {text}")
    
    def select_option(self, description, xpath, visible_text, max_attempts=3):
        """Seleciona uma opção em um select"""
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"📋 Tentativa {attempt} - Selecionando {visible_text}")
                
                element = self.wait_for_element(description, xpath)
                select = Select(element)
                select.select_by_visible_text(visible_text)
                
                print(f"✅ Selecionou: {visible_text}")
                return
                
            except (NoElementException, StaleElementReferenceException) as e:
                print(f"⚠️ Tentativa {attempt} falhou: {type(e).__name__}")
                if attempt < max_attempts:
                    time.sleep(2)
        
        raise RuntimeError(f"Falha ao selecionar {visible_text} após {max_attempts} tentativas")
    
    # ============================================================================
    # UTILITÁRIOS
    # ============================================================================
    
    def wait(self, seconds):
        """Aguarda um tempo específico"""
        print(f"⏳ Aguardando {seconds} segundos...")
        
        for i in range(seconds):
            print(f"\r⏳ {i + 1}/{seconds} segundos", end='', flush=True)
            time.sleep(1)
        
        print("\n✅ Aguardou com sucesso")
    
    def take_screenshot(self, filename):
        """Tira uma screenshot"""
        try:
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot salva: {filename}")
        except Exception as e:
            print(f"⚠️ Erro ao salvar screenshot: {e}")
    
    def _handle_timeout_error(self, description, xpath):
        """Trata erros de timeout"""
        print(f"❌ Timeout: {description}")
        
        # Salva screenshot
        filename = f"error_{description.lower().replace(' ', '_')}.png"
        self.take_screenshot(filename)
        
        # Salva HTML
        try:
            html_filename = f"error_{description.lower().replace(' ', '_')}.html"
            with open(html_filename, "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print(f"📄 HTML salvo: {html_filename}")
        except Exception as e:
            print(f"⚠️ Erro ao salvar HTML: {e}")
