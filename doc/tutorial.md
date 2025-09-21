# Tutorial: Configurando o Ambiente e Compilando o `loc`

Este guia apresenta um passo a passo completo para configurar o ambiente de desenvolvimento do `loc` usando `pipenv` e, em seguida, compilar a ferramenta em um executável (`.exe`) com `PyInstaller`.

## 1. Pré-requisitos

Antes de iniciar, garanta que você tenha os seguintes softwares instalados:

-   **Python 3.7 ou superior**: [Download do Python](https://www.python.org/downloads/)
-   **Git**: [Download do Git](https://git-scm.com/downloads/)
-   **Pipenv**: É o gerenciador de ambientes e dependências que usaremos. Se você não o tiver, instale-o globalmente com o `pip`:
    ```bash
    pip install pipenv
    ```

## 2. Configurando o Ambiente de Desenvolvimento

Esta seção mostra como preparar o projeto para execução a partir do código-fonte.

#### **Passo 2.1: Obtenha o Código-Fonte**

Primeiro, clone o repositório do projeto para a sua máquina local e navegue até a pasta criada.

```bash
git clone [https://github.com/seu-usuario/loc.git](https://github.com/seu-usuario/loc.git)
cd loc
```

#### **Passo 2.2: Instale as Dependências com `pipenv`**

O `pipenv` irá criar um ambiente virtual isolado para o projeto e instalar todas as dependências listadas no arquivo `Pipfile`.

Execute o seguinte comando na raiz do projeto:

```bash
pipenv install --dev
```

-   **O que este comando faz?**
    -   Ele lê o `Pipfile` para encontrar as dependências.
    -   Cria um ambiente virtual exclusivo para este projeto.
    -   Instala as dependências de produção (como `gitignore-parser`).
    -   A flag `--dev` garante que as dependências de desenvolvimento (como `pyinstaller`) também sejam instaladas.

## 3. Executando a Ferramenta via Script

Com o ambiente configurado, você pode executar o `loc` diretamente.

Para executar um script dentro do ambiente gerenciado pelo `pipenv`, utilize o comando `pipenv run`.

```bash
pipenv run python loc.py "C:\caminho\para\analisar"
```

Para especificar um nome de arquivo de saída, use a opção `-o`:

```bash
pipenv run python loc.py "C:\caminho\para\analisar" -o "meu_relatorio.json"
```

## 4. Gerando o Executável (`loc.exe`)

Para distribuir sua ferramenta, você pode compilá-la em um único arquivo `.exe`.

#### **Passo 4.1: Execute o PyInstaller via `pipenv`**

Como o `pyinstaller` foi instalado como uma dependência de desenvolvimento, você deve executá-lo também com o `pipenv run`.

```bash
pipenv run pyinstaller --onefile --name="loc" loc.py
```

-   `--onefile`: Cria um único arquivo executável.
-   `--name="loc"`: Define o nome do arquivo de saída como `loc.exe`.

#### **Passo 4.2: Localize o Arquivo Gerado**

O executável final estará na pasta `dist`, que será criada na raiz do seu projeto.

-   **Arquivo:** `dist/loc.exe`

## 5. Utilizando o Executável Final

O arquivo `loc.exe` é portátil. Você pode movê-lo para qualquer lugar em seu sistema Windows e executá-lo a partir de um terminal (CMD ou PowerShell).

```powershell
# Navegue até a pasta onde está o loc.exe
.\loc.exe "C:\caminho\de\outro\projeto" --output "relatorio_final.json"
```

Pronto! Agora você tem um fluxo de trabalho completo e profissional para desenvolver, testar e distribuir sua ferramenta `loc`.