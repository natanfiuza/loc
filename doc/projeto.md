


-----

### 1\. Código Atualizado (`contador_de_linhas.py`)

Abaixo está o script modificado. A principal alteração está no método `salvar_resultado_em_json` para calcular e adicionar o total geral de linhas.

```python
# -*- coding: utf-8 -*-

import os
import json
import argparse
import time

class ContadorDeLinhas:
    """
    Uma classe para encapsular a lógica de contagem de linhas em um projeto.
    """
    def __init__(self, caminho_do_projeto):
        """
        Inicializa o contador com o caminho do projeto alvo.
        """
        self.caminho_do_projeto = caminho_do_projeto
        self.contagem_por_extensao = {}
        # Lista de diretórios a serem ignorados na contagem.
        self.diretorios_ignorados = [
            '.git', 'node_modules', 'vendor', '.vscode', '.idea', '__pycache__', 'dist', 'build'
        ]
        # Lista de arquivos específicos a serem ignorados.
        self.arquivos_ignorados = [
            'package-lock.json', 'composer.lock'
        ]

    def executar_contagem(self):
        """
        Método principal que percorre os diretórios e executa a contagem.
        """
        print(f"Iniciando a análise do projeto em: {self.caminho_do_projeto}")
        start_time = time.time()

        for raiz, diretorios, arquivos in os.walk(self.caminho_do_projeto):
            # Remove os diretórios ignorados da lista de próximos a serem visitados
            diretorios[:] = [d for d in diretorios if d not in self.diretorios_ignorados]

            for nome_do_arquivo in arquivos:
                if nome_do_arquivo in self.arquivos_ignorados:
                    continue

                _, extensao = os.path.splitext(nome_do_arquivo)
                
                if not extensao:
                    continue
                
                extensao = extensao.lower()

                caminho_completo_do_arquivo = os.path.join(raiz, nome_do_arquivo)
                
                self._contar_linhas_do_arquivo(caminho_completo_do_arquivo, extensao)

        end_time = time.time()
        print(f"Análise concluída em {end_time - start_time:.2f} segundos.")
        return self.contagem_por_extensao

    def _contar_linhas_do_arquivo(self, caminho_do_arquivo, extensao):
        """
        Conta as linhas de um único arquivo e atualiza o dicionário de contagem.
        """
        try:
            with open(caminho_do_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
                numero_de_linhas = sum(1 for _ in arquivo)
            
            if extensao not in self.contagem_por_extensao:
                self.contagem_por_extensao[extensao] = {'total_linhas': 0, 'total_arquivos': 0}
            
            self.contagem_por_extensao[extensao]['total_linhas'] += numero_de_linhas
            self.contagem_por_extensao[extensao]['total_arquivos'] += 1

        except Exception as e:
            print(f"Erro ao ler o arquivo {caminho_do_arquivo}: {e}")

    def salvar_resultado_em_json(self, nome_do_arquivo_saida='resultado_contagem.json'):
        """
        Salva o dicionário com os resultados em um arquivo JSON, incluindo o total geral.
        """
        # NOVA IMPLEMENTAÇÃO: Calcula o total de linhas de todas as extensões somadas.
        total_geral_linhas = sum(dados['total_linhas'] for dados in self.contagem_por_extensao.values())

        # Estrutura final do JSON que será salvo.
        resultado_final = {
            'contagem_por_extensao': self.contagem_por_extensao,
            'total_geral_linhas_do_projeto': total_geral_linhas
        }

        try:
            with open(nome_do_arquivo_saida, 'w', encoding='utf-8') as json_file:
                json.dump(resultado_final, json_file, indent=4, ensure_ascii=False)
            print(f"Resultados salvos com sucesso no arquivo: {nome_do_arquivo_saida}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo JSON: {e}")

def main():
    """
    Função principal que configura os argumentos da linha de comando e executa o script.
    """
    parser = argparse.ArgumentParser(
        description="Conta as linhas de código de um projeto, agrupando por extensão de arquivo."
    )
    parser.add_argument(
        "caminho", 
        help="O caminho para a pasta do projeto que você deseja analisar."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.caminho):
        print(f"Erro: O caminho '{args.caminho}' não é um diretório válido.")
        return

    contador = ContadorDeLinhas(args.caminho)
    contador.executar_contagem()
    contador.salvar_resultado_em_json()

if __name__ == "__main__":
    main()
```

### 2\. Explicação das Alterações no Código

A única alteração funcional foi no método `salvar_resultado_em_json`:

1.  **Cálculo do Total Geral**:

    ```python
    total_geral_linhas = sum(dados['total_linhas'] for dados in self.contagem_por_extensao.values())
    ```

      * Esta linha usa uma "generator expression" para somar o valor da chave `'total_linhas'` de cada item no dicionário `contagem_por_extensao`. É uma forma concisa e eficiente de fazer a soma total.

2.  **Nova Estrutura do JSON**:

    ```python
    resultado_final = {
        'contagem_por_extensao': self.contagem_por_extensao,
        'total_geral_linhas_do_projeto': total_geral_linhas
    }
    ```

      * Criei um novo dicionário chamado `resultado_final`. Agora, o resultado original fica aninhado sob a chave `'contagem_por_extensao'`, e o novo total geral é adicionado como uma chave de nível superior.

3.  **Salvar o Novo Formato**:

    ```python
    json.dump(resultado_final, json_file, indent=4, ensure_ascii=False)
    ```

      * O `json.dump` agora salva este novo dicionário `resultado_final`.

Com isso, o arquivo `resultado_contagem.json` terá o seguinte formato:

```json
{
    "contagem_por_extensao": {
        ".php": {
            "total_linhas": 70000,
            "total_arquivos": 521
        },
        ".js": {
            "total_linhas": 120000,
            "total_arquivos": 315
        },
        ".css": {
            "total_linhas": 8500,
            "total_arquivos": 45
        }
    },
    "total_geral_linhas_do_projeto": 198500
}
```

-----

### 3\. Conteúdo para o `README.md`

Este é um `README.md` completo e bem detalhado. Você pode simplesmente copiar e colar este conteúdo em um novo arquivo chamado `README.md` na raiz do seu projeto.

````markdown
# Contador de Linhas de Código

Uma ferramenta de linha de comando simples e eficiente, escrita em Python, para contar o número de linhas de código em um projeto. A contagem é agrupada por extensão de arquivo e um total geral é fornecido.

## Funcionalidades

- **Contagem Recursiva**: Analisa todos os arquivos em um diretório e seus subdiretórios.
- **Agrupamento por Extensão**: Agrupa a contagem de linhas e arquivos por extensão (ex: `.py`, `.js`, `.php`).
- **Diretórios Ignorados**: Ignora automaticamente pastas comuns de dependências e metadados, como `node_modules`, `vendor`, `.git`, etc., para uma contagem mais precisa do código-fonte.
- **Saída em JSON**: Gera um arquivo `resultado_contagem.json` com os resultados detalhados e o total geral de linhas do projeto.
- **Portátil**: Pode ser facilmente compilado em um único executável (`.exe`) para uso em sistemas Windows sem a necessidade de instalar o Python.

## Pré-requisitos

- Python 3.6 ou superior.

## Como Usar (Script Python)

1.  **Clone ou baixe este repositório.**
2.  **Abra um terminal** (CMD, PowerShell, etc.) na pasta do projeto.
3.  **Execute o script**, passando o caminho do diretório que você deseja analisar como argumento.

    **Sintaxe:**
    ```bash
    python contador_de_linhas.py "C:\caminho\para\seu\projeto"
    ```

    *Observação: Use aspas ao redor do caminho se ele contiver espaços.*

4.  **Verifique a saída**: Um arquivo chamado `resultado_contagem.json` será criado no diretório atual.

### Exemplo de Saída (`resultado_contagem.json`)

```json
{
    "contagem_por_extensao": {
        ".php": {
            "total_linhas": 70000,
            "total_arquivos": 521
        },
        ".js": {
            "total_linhas": 120000,
            "total_arquivos": 315
        },
        ".css": {
            "total_linhas": 8500,
            "total_arquivos": 45
        }
    },
    "total_geral_linhas_do_projeto": 198500
}
```

## Criando um Executável (`.exe`) no Windows

Para maior portabilidade, você pode gerar um arquivo `.exe` que não depende de uma instalação do Python para ser executado.

1.  **Instale o PyInstaller**:
    ```bash
    pip install pyinstaller
    ```

2.  **Navegue até a pasta do script** e execute o seguinte comando no terminal:
    ```bash
    pyinstaller --onefile --name="ContadorDeLinhas" contador_de_linhas.py
    ```
    - `--onefile`: Agrupa tudo em um único arquivo executável.
    - `--name`: Define o nome do arquivo de saída.

3.  **Encontre o executável**: O arquivo `ContadorDeLinhas.exe` estará dentro de uma nova pasta chamada `dist`.

### Como Usar o Executável

Copie o arquivo `.exe` da pasta `dist` para qualquer local de sua preferência. Para usá-lo, abra um terminal nesse local e execute o comando:

```powershell
.\ContadorDeLinhas.exe "C:\caminho\para\seu\projeto"
```

O arquivo `resultado_contagem.json` será gerado no mesmo diretório onde o comando foi executado.

## Contribuição

Sinta-se à vontade para abrir *issues* ou enviar *pull requests* para melhorias e correções.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
````

Agora seu projeto está muito mais robusto, Natan\! A ferramenta é mais informativa e a documentação no `README.md` torna-a acessível para qualquer pessoa.