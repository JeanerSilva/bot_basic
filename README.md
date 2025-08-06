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

Eventuais ajustes devem ser feitos no main_eddge.py nas seguintes linhas

```python
caminho = os.path.expandvars(r'%LOCALAPPDATA%\\Microsoft\\Edge\\User Data')
...    
edge_options.add_argument('--profile-directory=Default')
```

A variável de sistema %LOCALAPPDATA% substitui "C:\\Users\\usuarioXXXXXXXX\\AppData\\Local"
O perfil encontrado, caso não seja o Default, deve ser trocado na string '--profile-directory='

## Uso

Edite o main.py para executar as funcionalidades necessárias.

O sistema usa o Microsoft Edge, que será fechado toda vez que a aplicação for usada.

O login no SIOP deve ser feito antes da execução do programa.

Todas as ações serão feitas em nome do usuário logado.

O acesso por meio da senha que foi logada se dá pelo uso do perfil padrão do Edge. 


## Trabalho com atividades sequenciais

Há um exemplo que lista um programa, limpa a tela e lista o próximo.
Os programas estão no arquivo lista.xlsx, aba Plan1 e cabeçalho "Programa"


