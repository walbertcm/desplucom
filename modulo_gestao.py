"""
Programa: Relatório de Desempenho do Quiz Educacional
Autor: Trabalho Final - Computação Aplicada à Prática Docente

Objetivo:
Ler os resultados de um quiz educacional a partir de uma planilha do Google Sheets
ou de um arquivo CSV local, calcular o aproveitamento dos participantes e gerar
um relatório textual para apoiar o acompanhamento docente.

Requisitos atendidos:
- Variáveis
- Entrada e saída de dados
- Estruturas condicionais
- Estruturas de repetição
- Funções
- Listas
- Manipulação de arquivos
"""

import csv
import urllib.request
from io import StringIO


# ============================================================
# 1. CONFIGURAÇÃO DA PLANILHA
# ============================================================

# Link base da sua planilha:
# https://docs.google.com/spreadsheets/d/1xPDsLk21UNBrRntw3QSL972H3LMPa5G0ZYI8Wjqiezg/edit?usp=sharing

# Para usar no Python, transforme o link em formato CSV:
# https://docs.google.com/spreadsheets/d/ID_DA_PLANILHA/export?format=csv&gid=GID_DA_ABA

# ID da planilha enviada pelo professor/usuário
ID_PLANILHA = "1xPDsLk21UNBrRntw3QSL972H3LMPa5G0ZYI8Wjqiezg"

# GID da aba.
# Normalmente, a primeira aba da planilha tem gid=0.
# Se você criar uma aba chamada "Resultados", clique nela e veja o gid no final do link.
GID_ABA_RESULTADOS = "397092477"

URL_PLANILHA_RESULTADOS = (
    f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv&gid={GID_ABA_RESULTADOS}"
)

ARQUIVO_LOCAL = "resultados_quiz.csv"
ARQUIVO_RELATORIO = "relatorio_desempenho.txt"


# ============================================================
# 2. FUNÇÕES DE CÁLCULO E CLASSIFICAÇÃO
# ============================================================

def calcular_percentual(acertos, total_questoes):
    """Calcula o percentual de acertos."""
    if total_questoes == 0:
        return 0
    return (acertos / total_questoes) * 100


def classificar_desempenho(percentual):
    """Classifica o desempenho conforme o percentual de acertos."""
    if percentual >= 80:
        return "Excelente desempenho"
    elif percentual >= 60:
        return "Bom desempenho"
    else:
        return "Baixo desempenho"


def gerar_recomendacao(percentual):
    """Gera uma recomendação pedagógica simples."""
    if percentual >= 80:
        return "Liberar o próximo nível ou propor atividade de aprofundamento."
    elif percentual >= 60:
        return "Revisar os pontos com erro e propor uma atividade intermediária."
    else:
        return "Retomar os conceitos principais antes de avançar para o próximo nível."


def converter_inteiro(valor):
    """Converte texto para inteiro, evitando erro caso a célula esteja vazia."""
    try:
        return int(str(valor).strip())
    except ValueError:
        return 0


# ============================================================
# 3. FUNÇÕES DE LEITURA DOS DADOS
# ============================================================

def carregar_dados_google_sheets(url):
    """
    Lê os dados de uma aba do Google Sheets em formato CSV.
    A planilha precisa estar compartilhada como 'qualquer pessoa com o link pode visualizar'
    ou publicada na web.
    """
    try:
        resposta = urllib.request.urlopen(url)
        conteudo = resposta.read().decode("utf-8")
        arquivo_csv = StringIO(conteudo)
        leitor = csv.DictReader(arquivo_csv)
        return list(leitor)

    except Exception as erro:
        print("\nErro ao carregar a planilha online.")
        print("Verifique se a planilha está compartilhada ou publicada na web.")
        print("Detalhes do erro:", erro)
        return []



# ============================================================
# 4. FUNÇÕES DE PROCESSAMENTO
# ============================================================

def processar_resultados(dados):
    """
    Recebe os dados brutos da planilha e calcula:
    - percentual de acertos;
    - classificação;
    - recomendação pedagógica.
    """
    resultados_processados = []

    for linha in dados:
        nome = linha.get("Nome", "").strip()
        turma = linha.get("Turma", "").strip()
        escola = linha.get("Escola", "").strip()
        email = linha.get("Email", "").strip()
        nivel = linha.get("Nivel", "").strip()
        atividade = linha.get("Atividade", "").strip()

        total_questoes = converter_inteiro(linha.get("TotalQuestoes", 0))
        acertos = converter_inteiro(linha.get("Acertos", 0))

        percentual = calcular_percentual(acertos, total_questoes)
        classificacao = classificar_desempenho(percentual)
        recomendacao = gerar_recomendacao(percentual)

        resultado = {
            "nome": nome,
            "email": email,
            "turma": turma,
            "escola": escola,
            "nivel": nivel,
            "atividade": atividade,
            "total_questoes": total_questoes,
            "acertos": acertos,
            "percentual": percentual,
            "classificacao": classificacao,
            "recomendacao": recomendacao
        }

        resultados_processados.append(resultado)

    return resultados_processados


# ============================================================
# 5. FUNÇÕES DE EXIBIÇÃO
# ============================================================

def exibir_relatorio_geral(resultados):
    """Mostra o relatório geral no terminal."""
    if not resultados:
        print("\nNenhum dado carregado.")
        return

    print("\n" + "=" * 60)
    print("RELATÓRIO GERAL DE DESEMPENHO")
    print("=" * 60)

    for item in resultados:
        print(f"\nParticipante: {item['nome']}")
        print(f"E-mail: {item['email']}")
        print(f"Turma: {item['turma']}")
        print(f"Escola: {item['escola']}")
        print(f"Nível: {item['nivel']}")
        print(f"Atividade: {item['atividade']}")
        print(f"Acertos: {item['acertos']} de {item['total_questoes']}")
        print(f"Aproveitamento: {item['percentual']:.2f}%")
        print(f"Classificação: {item['classificacao']}")
        print(f"Recomendação: {item['recomendacao']}")
        print("-" * 60)


def consultar_participante(resultados):
    """Consulta o desempenho de um participante pelo nome ou e-mail."""
    if not resultados:
        print("\nNenhum dado carregado.")
        return

    busca = input("\nDigite o nome ou e-mail do participante: ").strip().lower()
    encontrados = []

    for item in resultados:
        if busca in item["nome"].lower() or busca in item["email"].lower():
            encontrados.append(item)

    if not encontrados:
        print("\nParticipante não encontrado.")
        return

    print("\nResultado da consulta:")
    for item in encontrados:
        print("-" * 60)
        print(f"Nome: {item['nome']}")
        print(f"E-mail: {item['email']}")
        print(f"Turma: {item['turma']}")
        print(f"Escola: {item['escola']}")
        print(f"Nível: {item['nivel']}")
        print(f"Atividade: {item['atividade']}")
        print(f"Aproveitamento: {item['percentual']:.2f}%")
        print(f"Classificação: {item['classificacao']}")
        print(f"Recomendação: {item['recomendacao']}")


def exibir_resumo_turma(resultados):
    """Exibe um resumo geral da turma."""
    if not resultados:
        print("\nNenhum dado carregado.")
        return

    total_participantes = len(resultados)
    soma_percentuais = 0
    total_excelente = 0
    total_bom = 0
    total_baixo = 0

    for item in resultados:
        soma_percentuais += item["percentual"]

        if item["classificacao"] == "Excelente desempenho":
            total_excelente += 1
        elif item["classificacao"] == "Bom desempenho":
            total_bom += 1
        else:
            total_baixo += 1

    media_turma = soma_percentuais / total_participantes

    print("\n" + "=" * 60)
    print("RESUMO DA TURMA")
    print("=" * 60)
    print(f"Total de registros analisados: {total_participantes}")
    print(f"Média geral da turma: {media_turma:.2f}%")
    print(f"Excelente desempenho: {total_excelente}")
    print(f"Bom desempenho: {total_bom}")
    print(f"Baixo desempenho: {total_baixo}")


# ============================================================
# 6. FUNÇÃO PARA GERAR ARQUIVO DE RELATÓRIO
# ============================================================

def gerar_relatorio_txt(resultados, nome_arquivo):
    """Gera um arquivo TXT com o relatório de desempenho."""
    if not resultados:
        print("\nNenhum dado carregado.")
        return

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("RELATÓRIO DE DESEMPENHO DO QUIZ EDUCACIONAL\n")
        arquivo.write("=" * 60 + "\n\n")

        for item in resultados:
            arquivo.write(f"Participante: {item['nome']}\n")
            arquivo.write(f"E-mail: {item['email']}\n")
            arquivo.write(f"Turma: {item['turma']}\n")
            arquivo.write(f"Escola: {item['escola']}\n")
            arquivo.write(f"Nível: {item['nivel']}\n")
            arquivo.write(f"Atividade: {item['atividade']}\n")
            arquivo.write(f"Acertos: {item['acertos']} de {item['total_questoes']}\n")
            arquivo.write(f"Aproveitamento: {item['percentual']:.2f}%\n")
            arquivo.write(f"Classificação: {item['classificacao']}\n")
            arquivo.write(f"Recomendação: {item['recomendacao']}\n")
            arquivo.write("-" * 60 + "\n")

    print(f"\nRelatório gerado com sucesso: {nome_arquivo}")


# ============================================================
# 7. MENU PRINCIPAL
# ============================================================

def menu():
    """Interface textual do programa."""
    dados_processados = []

    while True:
        print("\n" + "=" * 60)
        print("SISTEMA DE RELATÓRIO DO QUIZ EDUCACIONAL")
        print("=" * 60)
        print("1 - Carregar dados do Google Sheets")
        print("2 - Exibir relatório geral")
        print("3 - Consultar participante")
        print("4 - Exibir resumo da turma")
        print("5 - Gerar relatório em TXT")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            dados = carregar_dados_google_sheets(URL_PLANILHA_RESULTADOS)
            dados_processados = processar_resultados(dados)
            print(f"\nDados carregados da planilha: {len(dados_processados)} registros.")

        elif opcao == "2":
            exibir_relatorio_geral(dados_processados)

        elif opcao == "3":
            consultar_participante(dados_processados)

        elif opcao == "4":
            exibir_resumo_turma(dados_processados)

        elif opcao == "5":
            gerar_relatorio_txt(dados_processados, ARQUIVO_RELATORIO)

        elif opcao == "0":
            print("\nPrograma encerrado.")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


# Executa o programa
if __name__ == "__main__":
    menu()
