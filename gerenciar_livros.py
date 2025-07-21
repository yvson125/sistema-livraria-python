
import PySimpleGUI as sg
import csv
import os
import sys
import subprocess

sg.theme('DarkGreen3')


def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def carregar_livros():
    caminho_arquivo = resource_path('livros.csv')
    if not os.path.exists(caminho_arquivo): return [], []
    cabecalho, dados = [], []
    try:
        with open(caminho_arquivo, mode='r', newline='', encoding='utf-8') as f:
            leitor = csv.reader(f)
            cabecalho = next(leitor)
            dados = [linha for linha in leitor]
    except Exception as e:
        sg.popup_error(f"Erro ao carregar livros.csv: {e}")
    return cabecalho, dados

def salvar_livros(cabecalho, dados):
    caminho_arquivo = resource_path('livros.csv')
    try:
        with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(cabecalho)
            escritor.writerows(dados)
        return True
    except Exception as e:
        sg.popup_error(f"Erro ao salvar livros.csv: {e}")
        return False


def criar_janela_edicao(livro_dados):
    layout_edicao = [
        [sg.Text('Título:'), sg.Input(livro_dados[0], key='-TITULO-')],
        [sg.Text('Autor:'), sg.Input(livro_dados[1], key='-AUTOR-')],
        [sg.Text('Categoria:'), sg.Input(livro_dados[2], key='-CATEGORIA-')],
        [sg.Text('Quantidade:'), sg.Input(livro_dados[3], key='-QUANTIDADE-')],
        [sg.Text('Preço (R$):'), sg.Input(livro_dados[4], key='-PRECO-')],
        [sg.Text('ISBN:'), sg.Input(livro_dados[5], key='-ISBN-')],
        [sg.Button('Salvar Alterações'), sg.Button('Cancelar')]
    ]
    janela_edicao = sg.Window('Editar Livro', layout_edicao)
    livro_atualizado = None
    while True:
        evento_ed, valores_ed = janela_edicao.read()
        if evento_ed in (sg.WINDOW_CLOSED, 'Cancelar'):
            break
        if evento_ed == 'Salvar Alterações':
            try:
                int(valores_ed['-QUANTIDADE-'])
                preco_float = float(valores_ed['-PRECO-'].replace(',', '.'))
                livro_atualizado = [
                    valores_ed['-TITULO-'],
                    valores_ed['-AUTOR-'],
                    valores_ed['-CATEGORIA-'],
                    valores_ed['-QUANTIDADE-'],
                    f"{preco_float:.2f}",
                    valores_ed['-ISBN-']
                ]
                break
            except ValueError:
                sg.popup_error('Quantidade deve ser um número inteiro e Preço deve ser um número válido.')
    janela_edicao.close()
    return livro_atualizado


python_exe = sys.executable
cabecalho_tabela, dados_tabela_mestra = carregar_livros()

layout = [
    [sg.Text('Gerenciamento de Livros', font=('Helvetica', 18))],
    [sg.Text('Filtrar:'), sg.Input(key='-FILTRO-', enable_events=True)],
    [sg.Table(values=dados_tabela_mestra, headings=cabecalho_tabela, max_col_width=25,
              auto_size_columns=True, display_row_numbers=True, justification='left',
              num_rows=15, key='-TABELA_LIVROS-', row_height=25)],
    [sg.Button('Cadastrar Novo Livro'),
     sg.Button('Editar Selecionado', button_color=('white', 'green')),
     sg.Button('Deletar Selecionado', button_color=('white', 'red'))]
]

janela = sg.Window('Painel de Livros', layout, resizable=True)
dados_exibidos_atualmente = dados_tabela_mestra

while True:
    evento, valores = janela.read()
    if evento == sg.WINDOW_CLOSED:
        break

    if evento == '-FILTRO-':
        termo_busca = valores['-FILTRO-'].lower()
        dados_filtrados = [
            livro for livro in dados_tabela_mestra
            if any(termo_busca in str(c).lower() for c in livro)
        ] if termo_busca else dados_tabela_mestra
        janela['-TABELA_LIVROS-'].update(values=dados_filtrados)
        dados_exibidos_atualmente = dados_filtrados

    if evento == 'Cadastrar Novo Livro':
        subprocess.Popen([python_exe, 'gui_cadastro_livro.py'])

    if evento in ('Editar Selecionado', 'Deletar Selecionado'):
        if valores['-TABELA_LIVROS-']:
            indice_na_tabela = valores['-TABELA_LIVROS-'][0]
            dados_do_livro = dados_exibidos_atualmente[indice_na_tabela]
            indice_real = dados_tabela_mestra.index(dados_do_livro)
            if evento == 'Editar Selecionado':
                dados_atualizados = criar_janela_edicao(dados_do_livro)
                if dados_atualizados:
                    dados_tabela_mestra[indice_real] = dados_atualizados
                    if salvar_livros(cabecalho_tabela, dados_tabela_mestra):
                        janela['-FILTRO-'].update(janela['-FILTRO-'].get())
                        sg.popup('Livro atualizado com sucesso!')
            elif evento == 'Deletar Selecionado':
                confirm = sg.popup_yes_no(f'Deletar "{dados_do_livro[0]}"?')
                if confirm == 'Yes':
                    dados_tabela_mestra.pop(indice_real)
                    if salvar_livros(cabecalho_tabela, dados_tabela_mestra):
                        janela['-FILTRO-'].update(janela['-FILTRO-'].get())
                        sg.popup('Livro deletado com sucesso!')
        else:
            sg.popup_error('Por favor, selecione um livro na tabela.')

janela.close()
