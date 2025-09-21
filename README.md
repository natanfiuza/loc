# loc - Contador de Linhas de Código

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

`loc` é uma ferramenta de linha de comando (CLI) eficiente, escrita em Python, para contar o número de linhas de código em um projeto. A contagem é agrupada por extensão de arquivo, e o relatório final é gerado em formato JSON.

O projeto utiliza o `pipenv` para um gerenciamento de dependências robusto e isolado.

## Funcionalidades Principais

-   **Análise Recursiva**: Percorre todos os diretórios e subdiretórios do projeto alvo.
-   **Integração com `.gitignore`**: Detecta e utiliza automaticamente o arquivo `.gitignore` do projeto analisado para excluir arquivos e pastas da contagem.
-   **Contagem por Extensão**: Agrupa o total de linhas e de arquivos por cada extensão (ex: `.py`, `.js`, `.php`).
-   **Relatório em JSON**: Gera um arquivo JSON com os resultados detalhados e o total geral de linhas.
-   **Saída Configurável**: Permite especificar o nome e o local do arquivo de relatório gerado.
-   **Compilável**: Pode ser facilmente compilado em um único executável (`.exe`) com PyInstaller.

## Dependências do Projeto

A ferramenta `loc` possui as seguintes dependências, gerenciadas pelo `pipenv`:

-   **Dependências de Produção:**
    -   `gitignore-parser`: Utilizada para interpretar as regras de arquivos `.gitignore`.

-   **Dependências de Desenvolvimento:**
    -   `pyinstaller`: Utilizada para gerar o arquivo executável (`.exe`).

## Instalação e Uso Rápido

Para começar a usar a ferramenta a partir do código-fonte:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/loc.git](https://github.com/seu-usuario/loc.git)
    cd loc
    ```

2.  **Instale as dependências com `pipenv`:**
    ```bash
    pipenv install --dev
    ```

3.  **Execute a análise:**
    ```bash
    pipenv run python loc.py "C:\caminho\para\seu\projeto" -o relatorio.json
    ```

## Como Usar

### Usando o Script Python (com `pipenv`)

```bash
pipenv run python loc.py <caminho_do_projeto> [opções]
```

### Usando o Executável (`loc.exe`)

```powershell
.\loc.exe <caminho_do_projeto> [opções]
```

### Opções

-   `<caminho_do_projeto>`: (Obrigatório) O caminho para a pasta do projeto que você deseja analisar.
-   `-o`, `--output`: (Opcional) Define o nome do arquivo JSON de saída. Padrão: `resultado_contagem.json`.

## Exemplo de Saída (`resultado_contagem.json`)

```json
{
    "contagem_por_extensao": {
        ".py": {
            "total_linhas": 1520,
            "total_arquivos": 15
        },
        ".js": {
            "total_linhas": 8734,
            "total_arquivos": 42
        }
    },
    "total_geral_linhas_do_projeto": 10254
}
```

## Tutorial de Configuração e Compilação

Para um guia detalhado sobre como configurar o ambiente do zero e compilar o executável, veja nosso **[TUTORIAL.md](TUTORIAL.md)**.

## Licença

Este projeto está sob a licença MIT.