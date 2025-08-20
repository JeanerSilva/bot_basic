# 🤖 PBI Bot - Versão Limpa

Bot automatizado para interação com sistemas web usando Selenium e Python, com arquitetura limpa e moderna.

## 🏗️ Arquitetura

### 📁 Estrutura de Diretórios
```
pbi-bot/
├── app.py                    # Aplicação principal
├── core/                     # Núcleo da aplicação
│   ├── __init__.py
│   ├── driver_manager.py     # Gerenciamento do driver
│   ├── element_manager.py    # Gerenciamento de elementos
│   └── web_actions.py        # Ações web
├── flows/                    # Fluxos de negócio
│   ├── __init__.py
│   ├── test_flow.py          # Fluxo de teste
│   └── powerbi_flow.py       # Fluxo de leitura do Power BI
├── utils/                    # Utilitários
│   ├── __init__.py
│   └── excel_utils.py        # Manipulação de Excel
├── config/                   # Configurações
│   ├── config.py
│   ├── elementos.json
│   └── urls.json
├── drivers/                  # Drivers dos navegadores
├── logs/                     # Logs da aplicação
└── requirements.txt
```

## 🚀 Como Executar

### Execução Normal
```bash
python app.py
```

### Execução Automática
```bash
python app.py /y
```

### Fluxo Específico do Power BI
```bash
python powerbi_main.py
```

Para execução automática:
```bash
python powerbi_main.py /y
```

## 🧪 Como Usar

### Fluxo do Power BI

O bot inclui um fluxo específico para ler valores do Power BI:

```python
from flows import powerbi_flow

# Executa o fluxo
valor = powerbi_flow(web_actions)
print(f"Valor lido: {valor}")
```

**Funcionalidades:**
- Abre automaticamente o Power BI no navegador
- Localiza e lê o valor dos "Objetivos Específicos"
- Usa múltiplas estratégias de localização para maior confiabilidade
- Captura screenshots em caso de erro

**URLs suportadas:**
- Power BI com visual de cartão mostrando "Objetivos Específicos 463"

### Criando um Novo Fluxo

```python
from core import WebActions

class MeuNovoFluxo:
    def __init__(self, web_actions: WebActions):
        self.web_actions = web_actions
    
    def execute(self):
        # Sua lógica aqui
        self.web_actions.navigate_to("minha_atividade")
        self.web_actions.fill_input("Campo", "elemento", "valor")
        self.web_actions.click("Botão", "//button[@id='salvar']")
        return True
```

### Adicionando Novos Elementos

Edite `config/elementos.json`:
```json
{
  "item": "novo_elemento",
  "xpath": "//div[@class='minha-classe']"
}
```

## 🔧 Principais Melhorias

1. **✅ Arquitetura Limpa**: Sem duplicações ou código legado
2. **✅ Separação de Responsabilidades**: Cada classe tem uma função específica
3. **✅ Métodos Modernos**: Nomes em inglês e padrões consistentes
4. **✅ Tratamento de Erros**: Screenshots e logs automáticos
5. **✅ Fácil Extensão**: Adicione novos fluxos sem modificar o core

## 📋 Dependências

```bash
pip install -r requirements.txt
```

## 🔍 Logs

- `logs/edge_driver.log` - Logs do driver do Edge
- Screenshots de erro são salvos automaticamente
- HTML da página é salvo em caso de erro

## 🎯 Próximos Passos

1. Implementar testes unitários
2. Adicionar logging estruturado
3. Criar mais fluxos de negócio
4. Implementar retry automático para falhas
5. Adicionar configuração via variáveis de ambiente

## 📚 Exemplos

### Exemplo do Power BI
```bash
python examples/exemplo_powerbi.py
```

## 💡 Exemplo de Uso Completo

```python
from core import DriverManager, ElementManager, WebActions
from flows import TestFlow

# Inicializa
driver_manager = DriverManager()
element_manager = ElementManager()

# Inicia driver
driver, wait = driver_manager.start_driver()

# Cria WebActions
web_actions = WebActions(
    driver=driver,
    wait=wait,
    actions=driver_manager.get_actions(),
    element_manager=element_manager
)

# Executa fluxo
test_flow = TestFlow(web_actions)
success = test_flow.execute()

# Encerra
driver_manager.shutdown()
```

## 🆕 Comparação com Versão Anterior

| Aspecto | Versão Anterior | Nova Versão |
|---------|----------------|-------------|
| Arquitetura | Monolítica | Modular |
| Duplicações | Muitas | Nenhuma |
| Nomes | Português | Inglês |
| Extensibilidade | Baixa | Alta |
| Manutenibilidade | Baixa | Alta |
| Testes | Difícil | Fácil |