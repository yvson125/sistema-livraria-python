# gui_registrar_venda.py 
import PySimpleGUI as sg
import csv
import os
import sys  
from datetime import datetime


def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def carregar_dados(nome_arquivo):
    caminho_arquivo = resource_path(nome_arquivo) 
    if not os.path.exists(caminho_arquivo): return []
    dados = []
    try:
        with open(caminho_arquivo, mode='r', newline='', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            dados = [linha for linha in leitor]
    except Exception as e:
        sg.popup_error(f"Erro ao carregar o arquivo {nome_arquivo}: {e}")
    return dados

def atualizar_estoque_csv(livros_atualizados):
    caminho_arquivo = resource_path('livros.csv') 
    try:
        with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            if livros_atualizados:
                campos = livros_atualizados[0].keys()
                escritor = csv.DictWriter(arquivo_csv, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(livros_atualizados)
        return True
    except Exception as e: sg.popup_error(f"Erro ao atualizar o estoque: {e}"); return False

def registrar_venda_csv(venda):
    caminho_arquivo = resource_path('vendas.csv') 
    arquivo_existe = os.path.isfile(caminho_arquivo)
    try:
        with open(caminho_arquivo, mode='a', newline='', encoding='utf-8') as f:
            campos = ['cpf_cliente', 'titulo_livro', 'quantidade', 'preco_unitario', 'valor_total', 'data_hora']
            escritor = csv.DictWriter(f, fieldnames=campos)
            if not arquivo_existe or f.tell() == 0:
                escritor.writeheader()
            escritor.writerow(venda)
        return True
    except Exception as e: sg.popup_error(f"Erro ao registrar a venda: {e}"); return False


livros = carregar_dados('livros.csv')
clientes = carregar_dados('clientes.csv')
opcoes_clientes = [f"{c['nome']} ({c['cpf']})" for c in clientes]
opcoes_livros = [l['titulo'] for l in livros]

layout = [
    [sg.Text('Cliente:', size=(10,1)), sg.Combo(opcoes_clientes, key='cliente_selecionado', size=(40,1), readonly=True)],
    [sg.Text('Livro:', size=(10,1)), sg.Combo(opcoes_livros, key='livro_selecionado', size=(40,1), readonly=True)],
    [sg.Text('Quantidade:', size=(10,1)), sg.Input(key='quantidade', size=(10,1))],
    [sg.Button('Registrar Venda', button_color=('white', 'purple'))],
    [sg.Text('', size=(50, 2), key='mensagem')]
]

janela = sg.Window('Registro de Vendas', layout)


while True:
    evento, valores = janela.read()
    if evento == sg.WINDOW_CLOSED: break
    if evento == 'Registrar Venda':
        cliente_str = valores['cliente_selecionado']
        livro_str = valores['livro_selecionado']
        quantidade_str = valores['quantidade']
        if not all([cliente_str, livro_str, quantidade_str]):
            janela['mensagem'].update('Por favor, preencha todos os campos.', text_color='red')
            continue
        try:
            quantidade_vendida = int(quantidade_str)
            if quantidade_vendida <= 0: raise ValueError()
        except ValueError:
            janela['mensagem'].update('Quantidade inválida.', text_color='red')
            continue
        livro_selecionado = next((l for l in livros if l['titulo'] == livro_str), None)
        cpf_cliente = cliente_str.split('(')[1].replace(')', '')
        if livro_selecionado and quantidade_vendida > int(livro_selecionado['quantidade']):
            janela['mensagem'].update(f"Estoque insuficiente! Apenas {livro_selecionado['quantidade']} unidades.", text_color='red')
            continue
        if livro_selecionado:
            preco_unitario = float(livro_selecionado['preco'])
            valor_total_venda = quantidade_vendida * preco_unitario
            livro_selecionado['quantidade'] = str(int(livro_selecionado['quantidade']) - quantidade_vendida)
            sucesso_estoque = atualizar_estoque_csv(livros)
            nova_venda = {
                'cpf_cliente': cpf_cliente, 'titulo_livro': livro_str,
                'quantidade': quantidade_vendida, 'preco_unitario': f"{preco_unitario:.2f}",
                'valor_total': f"{valor_total_venda:.2f}",
                'data_hora': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            sucesso_venda = registrar_venda_csv(nova_venda)
            if sucesso_estoque and sucesso_venda:
                msg = f'Venda registrada! Valor Total: R$ {valor_total_venda:.2f}'
                janela['mensagem'].update(msg, text_color='green')
                janela['cliente_selecionado'].update(''); janela['livro_selecionado'].update(''); janela['quantidade'].update('')
            else:
                janela['mensagem'].update('Ocorreu um erro.', text_color='red')
        else:
            janela['mensagem'].update('Erro: Livro não encontrado.', text_color='red')
janela.close()