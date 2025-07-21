# gui_relatorio_estoque.py (Versão final e robusta)
import PySimpleGUI as sg
import csv
import os
import sys  # Adicionado
from datetime import datetime

# --- FUNÇÃO DE CAMINHO ROBUSTA ---
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- FUNÇÕES DE CÁLCULO (Atualizadas para usar resource_path) ---
def carregar_dados(nome_arquivo):
    caminho_arquivo = resource_path(nome_arquivo) # USA A FUNÇÃO
    if not os.path.exists(caminho_arquivo): return []
    dados = []
    try:
        with open(caminho_arquivo, mode='r', newline='', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            dados = [linha for linha in leitor]
    except Exception as e: sg.popup_error(f"Erro ao carregar o arquivo {nome_arquivo}: {e}"); return []
    return dados

def calcular_receita_por_livro():
    vendas = carregar_dados('vendas.csv')
    receita_por_livro = {}
    for venda in vendas:
        titulo = venda['titulo_livro']
        valor_total = float(venda['valor_total'])
        receita_por_livro[titulo] = receita_por_livro.get(titulo, 0) + valor_total
    return receita_por_livro

def calcular_valor_estoque_por_categoria():
    livros = carregar_dados('livros.csv')
    valor_por_categoria = {}
    for livro in livros:
        categoria = livro['categoria']
        valor_item = int(livro['quantidade']) * float(livro['preco'])
        valor_por_categoria[categoria] = valor_por_categoria.get(categoria, 0) + valor_item
    return valor_por_categoria

# --- LAYOUT E LÓGICA DO RELATÓRIO (Sua lógica, sem alterações) ---
layout = [
    [sg.Text('Relatório Financeiro e de Estoque', font=('Helvetica', 16))],
    [sg.Button('Gerar Relatório Atualizado', size=(30, 2))],
    [sg.Multiline(size=(80, 35), key='-RELATORIO-', disabled=True, background_color='light gray', text_color='black')]
]
janela = sg.Window('Relatório Gerencial - Livraria', layout, element_justification='c')

while True:
    evento, valores = janela.read()
    if evento == sg.WINDOW_CLOSED: break
    if evento == 'Gerar Relatório Atualizado':
        receita_livro = calcular_receita_por_livro()
        valor_estoque_categoria = calcular_valor_estoque_por_categoria()
        livros_em_estoque = carregar_dados('livros.csv')
        vendas_detalhadas = carregar_dados('vendas.csv')
        clientes = carregar_dados('clientes.csv')

        mapa_clientes = {cliente['cpf']: cliente['nome'] for cliente in clientes}
        
        data_hora_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        texto_relatorio = f"Relatório Gerado em: {data_hora_atual}\n"
        texto_relatorio += "="*60 + "\n\n"
        
        texto_relatorio += "--- RECEITA TOTAL POR LIVRO ---\n"
        receita_total_geral = sum(float(v['valor_total']) for v in vendas_detalhadas)
        if not receita_livro:
            texto_relatorio += "Nenhuma venda registrada.\n"
        else:
            for livro, total in receita_livro.items():
                texto_relatorio += f"- {livro}: R$ {total:.2f}\n"
        texto_relatorio += f"\n>> RECEITA TOTAL DE VENDAS: R$ {receita_total_geral:.2f}\n"
        
        texto_relatorio += "\n" + "="*60 + "\n\n"
        
        texto_relatorio += "--- VALOR DO ESTOQUE POR CATEGORIA ---\n"
        valor_total_estoque = sum(int(l['quantidade']) * float(l['preco']) for l in livros_em_estoque)
        if not valor_estoque_categoria:
            texto_relatorio += "Nenhum livro em estoque.\n"
        else:
            for categoria, total in valor_estoque_categoria.items():
                texto_relatorio += f"- {categoria}: R$ {total:.2f}\n"
        texto_relatorio += f"\n>> VALOR TOTAL DO ESTOQUE: R$ {valor_total_estoque:.2f}\n"

        texto_relatorio += "\n" + "="*60 + "\n\n"

        texto_relatorio += "--- ESTOQUE INDIVIDUAL POR LIVRO ---\n"
        if not livros_em_estoque:
            texto_relatorio += "Nenhum livro cadastrado.\n"
        else:
            for livro in livros_em_estoque:
                texto_relatorio += f"- {livro['titulo']}: {livro['quantidade']} unidades\n"
        
        texto_relatorio += "\n" + "="*60 + "\n\n"
        texto_relatorio += "--- HISTÓRICO DE VENDAS DETALHADO ---\n"
        if not vendas_detalhadas:
            texto_relatorio += "Nenhuma venda registrada.\n"
        else:
            vendas_detalhadas.sort(key=lambda v: datetime.strptime(v['data_hora'], "%d/%m/%Y %H:%M:%S"), reverse=True)
            
            for venda in vendas_detalhadas:
                cpf_cliente = venda['cpf_cliente']
                nome_cliente = mapa_clientes.get(cpf_cliente, f"CPF {cpf_cliente}")
                
                texto_relatorio += (f"- Data: {venda['data_hora']} | "
                                    f"Cliente: {nome_cliente} | "
                                    f"Livro: {venda['titulo_livro']} | "
                                    f"Qtd: {venda['quantidade']}\n")

        janela['-RELATORIO-'].update(texto_relatorio)

janela.close()