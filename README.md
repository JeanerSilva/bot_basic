# SIOP-BOT

## Configuração

### Aplicação
Use esta aplicação para acessar o SIOP de forma automatizada.

Com o python instalado, crie o ambiente virtual:

```shell
python -m venv .venv
```

Após, instale as bibliotecas necessárias

```shell
pip install -r requirements.txt
```

Acesse o ambiente virtual:

```shell
.venv\Scripts\activate
```

### Perfil

Para confirmar a pasta e o perfil execute:
```shell
python perfis.py
```

Resultado esperado:

```shell
--user-data-dir=C:\\Users\\usuarioXXXXXXXX\\AppData\\Local\\Microsoft\\Edge\\User Data
Perfil encontrado: Default
```

Eventuais ajustes devem ser feitos em config/config.py nas seguintes linhas

```python
EDGE_DIR = r'%LOCALAPPDATA%\\Microsoft\\Edge\\User Data'
PERFIL_PADRAO = "Default"
```
A variável de sistema %LOCALAPPDATA% substitui "C:\\Users\\usuarioXXXXXXXX\\AppData\\Local"

## Uso

Edite o siop_bot.py para executar as funcionalidades necessárias.

O sistema usa o Microsoft Edge, que será fechado toda vez que a aplicação for usada.

O login no SIOP deve ser feito antes da execução do programa.

Todas as ações serão feitas em nome do usuário logado.

O acesso por meio da senha que foi logada se dá pelo uso do perfil padrão do Edge. 


## Acréscimos de novas funcionalidades

Verificar se há existe a url em config/urls.json

Avaliar o tipo de interação necessário:
- preenhcer input ou textarea
- preencher seletor
- clicar botão

No caso de input ou textarea:
- Procurar o xpath de cada item e adicionar no arquivo elementos.json.
- Verificar qual arquivo deve ser alterado na pasta flow:
-- programas.py: trabalha com a tela de todos os programas selecionados
-- programa.py: trabaha com um programa específico.
-- objetivos_específicos.py: trabalha com a tela de todos os objetivos específicos selecionados
-- objetivo_específico.py: trabalha com um objetivo específico específico
-- entregas.py: trabalha com a tela de todos as entregas selecionados
-- entrega.py: trabalha com uma entrega específica
- adicionar um fluxo personalizado
-- avalie se a função desejada já consta no arquivo siop_utils.py
-- se já existir, apenas adiconar no arquivo de fluxo com sb.função



No caso dos botões, deve-se saber o tipo e o valor.

No caso de tabelas, deve-se pegar o xpath do /thead