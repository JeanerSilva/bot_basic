"""
Configuração para testes usando pytest
"""

import pytest
from unittest.mock import Mock, MagicMock
from core import WebActions, ElementManager


@pytest.fixture
def mock_driver():
    """Mock do driver do Selenium"""
    driver = Mock()
    driver.execute_script.return_value = True
    driver.save_screenshot.return_value = None
    driver.page_source = "<html><body>Test</body></html>"
    return driver


@pytest.fixture
def mock_wait():
    """Mock do WebDriverWait"""
    wait = Mock()
    return wait


@pytest.fixture
def mock_actions():
    """Mock do ActionChains"""
    actions = Mock()
    actions.move_by_offset.return_value = actions
    actions.click.return_value = actions
    actions.send_keys.return_value = actions
    actions.perform.return_value = None
    return actions


@pytest.fixture
def mock_element_manager():
    """Mock do ElementManager"""
    element_manager = Mock()
    element_manager.get_xpath_elemento.return_value = "//test[@id='test']"
    element_manager.get_url.return_value = "/test"
    return element_manager


@pytest.fixture
def web_actions(mock_driver, mock_wait, mock_actions, mock_element_manager):
    """Instância de WebActions com mocks"""
    return WebActions(
        driver=mock_driver,
        wait=mock_wait,
        actions=mock_actions,
        element_manager=mock_element_manager
    )


@pytest.fixture
def element_manager():
    """Instância real de ElementManager para testes de integração"""
    return ElementManager()
