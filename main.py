# -*- coding: utf-8 -*-

import os
import json
import argparse
import time
from gitignore_parser import parse_gitignore
from tqdm import tqdm 

class LineCodeCounter:
    """
    Uma classe para encapsular a lógica de contagem de linhas em um projeto.
    """
    def __init__(self, caminho_do_projeto):
        """
        Inicializa o contador com o caminho do projeto alvo.
        """
        self.caminho_do_projeto = caminho_do_projeto
        self.contagem_por_extensao = {}
        # Lista de diretórios a serem ignorados na contagem (fallback).
        self.diretorios_ignorados = [
            '.git', 'node_modules', 'vendor', '.vscode', '.idea', '__pycache__', 'dist', 'build'
        ]
        # Lista de arquivos específicos a serem ignorados (fallback).
        self.arquivos_ignorados = [
            'package-lock.json', 'composer.lock'
        ]
        
        # Lógica para carregar o .gitignore
        self.gitignore_parser = None
        caminho_gitignore = os.path.join(self.caminho_do_projeto, '.gitignore')
        if os.path.exists(caminho_gitignore):
            print("Arquivo .gitignore encontrado. Usando suas regras.")
            self.gitignore_parser = parse_gitignore(caminho_gitignore, self.caminho_do_projeto)
        else:
            print("Arquivo .gitignore não encontrado. Usando a lista de ignorados padrão.")

    def executar_contagem(self):
        """
        Método principal que percorre os diretórios e executa a contagem,
        exibindo uma barra de progresso de passagem única com post-fix.
        """
        start_time = time.time()
        
        # ALTERADO: Lógica de passagem única, sem total pré-calculado.
        # 'leave=False' faz a barra desaparecer após a conclusão. Mude para True se quiser que ela permaneça.
        with tqdm(desc="Analisando", unit=" arq", unit_scale=True, leave=True, ncols=100) as pbar:
            for raiz, diretorios, arquivos in os.walk(self.caminho_do_projeto):
                # Mantém a otimização de ignorar diretórios conhecidos
                diretorios[:] = [d for d in diretorios if d not in self.diretorios_ignorados]
                
                # NOVO: Obtém o caminho relativo para uma exibição mais limpa
                caminho_relativo = os.path.relpath(raiz, self.caminho_do_projeto)
                # Trata o caso da pasta raiz para não exibir um ponto "."
                if caminho_relativo == '.':
                    caminho_relativo = self.caminho_do_projeto.split(os.sep)[-1]

                for nome_do_arquivo in arquivos:
                    # NOVO: Atualiza o post-fix da barra com a localização atual
                    pbar.set_postfix_str(f"Em: {caminho_relativo}", refresh=False)

                    caminho_completo_do_arquivo = os.path.join(raiz, nome_do_arquivo)

                    # As verificações de arquivos a ignorar continuam as mesmas
                    if self.gitignore_parser and self.gitignore_parser(caminho_completo_do_arquivo):
                        continue
                    if nome_do_arquivo in self.arquivos_ignorados:
                        continue
                    if not self._e_arquivo_de_texto(caminho_completo_do_arquivo):
                        continue

                    _, extensao = os.path.splitext(nome_do_arquivo)
                    
                    if not extensao:
                        extensao = "sem_extensao"
                    else:
                        extensao = extensao.lower()
                    
                    self._contar_linhas_do_arquivo(caminho_completo_do_arquivo, extensao)
                    
                    # Atualiza a contagem de arquivos processados na barra
                    pbar.update(1)

        end_time = time.time()
        # NOVO: Calcula o total de arquivos processados a partir dos resultados para um sumário final
        total_arquivos_processados = sum(data['total_arquivos'] for data in self.contagem_por_extensao.values())
        print(f"\nAnálise concluída em {end_time - start_time:.2f} segundos.")
        print(f"Total de {total_arquivos_processados} arquivos analisados.")
        return self.contagem_por_extensao

    def _contar_linhas_do_arquivo(self, caminho_do_arquivo, extensao):
        """
        Conta as linhas de um único arquivo, obtém seu tamanho em bytes,
        e atualiza o dicionário de contagem.
        """
        try:
            # Obtém o tamanho do arquivo em bytes
            tamanho_em_bytes = os.path.getsize(caminho_do_arquivo)

            with open(caminho_do_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
                numero_de_linhas = sum(1 for _ in arquivo)
            
            # ALTERADO: Adiciona a chave 'total_bytes' ao inicializar uma nova extensão
            if extensao not in self.contagem_por_extensao:
                self.contagem_por_extensao[extensao] = {'total_linhas': 0, 'total_arquivos': 0, 'total_bytes': 0}
            
            self.contagem_por_extensao[extensao]['total_linhas'] += numero_de_linhas
            self.contagem_por_extensao[extensao]['total_arquivos'] += 1
            # Acumula o total de bytes para a extensão
            self.contagem_por_extensao[extensao]['total_bytes'] += tamanho_em_bytes

        except Exception as e:
            print(f"Erro ao ler o arquivo {caminho_do_arquivo}: {e}")

    def salvar_resultado_em_json(self, nome_do_arquivo_saida='resultado_contagem.json'):
        """
        Salva o dicionário com os resultados em um arquivo JSON, incluindo o total geral.
        """
        # Calcula o total de linhas de todas as extensões somadas.
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

    def _e_arquivo_de_texto(self, caminho_do_arquivo):
            """
            Verifica se um arquivo é provavelmente um arquivo de texto.
            A heurística é ler um pedaço do arquivo e checar a ausência de bytes nulos.
            """
            try:
                with open(caminho_do_arquivo, 'rb') as f:
                    # Lê os primeiros 4KB, o que é suficiente para a maioria dos casos
                    chunk = f.read(4096)
                    # Arquivos de texto (ASCII/UTF-8) não devem conter o byte nulo
                    return b'\0' not in chunk
            except Exception:
                # Em caso de erro de leitura, assume que não é um arquivo que queremos processar
                return False
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
    # Parâmetro opcional para o nome do arquivo de saída
    parser.add_argument(
        "-o", "--output",
        default="resultado_contagem.json",
        help="Caminho e nome do arquivo JSON de saída para o relatório. (Padrão: resultado_contagem.json)"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.caminho):
        print(f"Erro: O caminho '{args.caminho}' não é um diretório válido.")
        return

    contador = LineCodeCounter(args.caminho)
    contador.executar_contagem()
    # Passa o nome do arquivo de saída para o método
    contador.salvar_resultado_em_json(args.output)
if __name__ == "__main__":
    main()