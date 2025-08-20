"""
Testes para a classe WebActions
"""

import pytest
from selenium.common.exceptions import TimeoutException
from core import WebActions
from unittest.mock import Mock


class TestWebActions:
    """Testes para WebActions"""
    
    def test_clica_na_tela(self, web_actions, mock_actions):
        """Testa clique em coordenadas específicas"""
        web_actions.clica_na_tela(100, 200)
        
        mock_actions.move_by_offset.assert_called_once_with(100, 200)
        mock_actions.click.assert_called_once()
        mock_actions.perform.assert_called_once()
    
    def test_digita(self, web_actions, mock_actions):
        """Testa digitação de texto"""
        web_actions.digita("texto teste")
        
        mock_actions.send_keys.assert_called_once_with("texto teste")
        mock_actions.perform.assert_called_once()
    
    def test_clica_na_tela_e_digita(self, web_actions, mock_actions):
        """Testa clique e digitação em coordenadas"""
        web_actions.clica_na_tela_e_digita(150, 250, "texto")
        
        mock_actions.move_by_offset.assert_called_once_with(150, 250)
        mock_actions.click.assert_called_once()
        mock_actions.send_keys.assert_called_once_with("texto")
        mock_actions.perform.assert_called()
    
    def test_acessa_url(self, web_actions, mock_driver, mock_element_manager):
        """Testa acesso a URL"""
        # Mock da configuração
        with pytest.MonkeyPatch().context() as m:
            m.setattr("config.config.URL_BASE", "https://exemplo.com")
            
            web_actions.acessa("minha_atividade")
            
            mock_element_manager.get_url.assert_called_once_with("minha_atividade")
            mock_driver.get.assert_called_once_with("https://exemplo.com/test")
    
    def test_aguarda_elemento_sucesso(self, web_actions, mock_wait):
        """Testa aguardar elemento com sucesso"""
        mock_element = Mock()
        mock_wait.until.return_value = mock_element
        
        # Mock do método aguarda_jquery
        with pytest.MonkeyPatch().context() as m:
            m.setattr(web_actions, "aguarda_jquery", Mock())
            
            resultado = web_actions.aguarda_elemento("Teste", "//test")
            
            assert resultado == mock_element
            mock_wait.until.assert_called_once()
    
    def test_aguarda_elemento_timeout(self, web_actions, mock_wait, mock_driver):
        """Testa timeout ao aguardar elemento"""
        mock_wait.until.side_effect = TimeoutException("Timeout")
        
        with pytest.raises(TimeoutException):
            web_actions.aguarda_elemento("Teste", "//test")
        
        mock_driver.save_screenshot.assert_called_once()
    
    def test_preenche_input_sucesso(self, web_actions, mock_element_manager):
        """Testa preenchimento de input com sucesso"""
        mock_element = Mock()
        
        # Mock do método aguarda_elemento
        with pytest.MonkeyPatch().context() as m:
            m.setattr(web_actions, "aguarda_elemento", Mock(return_value=mock_element))
            
            web_actions.preenche_input("Campo", "elemento", "valor")
            
            mock_element.clear.assert_called_once()
            mock_element.send_keys.assert_called_once_with("valor")
    
    def test_espera(self, web_actions):
        """Testa função de espera"""
        with pytest.MonkeyPatch().context() as m:
            m.setattr("time.sleep", Mock())
            
            web_actions.espera(3)
            
            # Verifica se sleep foi chamado 3 vezes
            assert m.getattr("time.sleep").call_count == 3
