
import PySimpleGUI as sg
import csv
import os
import sys
import subprocess

#  FUNÇÃO DE CAMINHO ROBUSTA 
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#  FUNÇÕES DE DADOS 
def carregar_clientes():
    caminho_arquivo = resource_path('clientes.csv')
    if not os.path.exists(caminho_arquivo): return [], []
    cabecalho, dados = [], []
    try:
        with open(caminho_arquivo, mode='r', newline='', encoding='utf-8') as f:
            leitor = csv.reader(f)
            cabecalho = next(leitor)
            dados = [linha for linha in leitor]
    except Exception as e:
        sg.popup_error(f"Erro ao carregar clientes.csv: {e}")
    return cabecalho, dados

def salvar_clientes(cabecalho, dados):
    caminho_arquivo = resource_path('clientes.csv')
    try:
        with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(cabecalho)
            escritor.writerows(dados)
        return True
    except Exception as e:
        sg.popup_error(f"Erro ao salvar clientes.csv: {e}")
        return False

# JANELA DE EDIÇÃO 
def criar_janela_edicao_cliente(cliente_dados):
    layout_edicao = [
        [sg.Text('Nome:'), sg.Input(cliente_dados[0], key='-NOME-')],
        [sg.Text('CPF:'), sg.Input(cliente_dados[1], key='-CPF-')],
        [sg.Text('Telefone:'), sg.Input(cliente_dados[2], key='-TELEFONE-')],
        [sg.Text('E-mail:'), sg.Input(cliente_dados[3], key='-EMAIL-')],
        [sg.Text('Endereço:'), sg.Input(cliente_dados[4], key='-ENDERECO-')],
        
        [sg.Button('Salvar Alterações'), sg.Button('Cancelar')]
    ]
    janela_edicao = sg.Window('Editar Cliente', layout_edicao)
    cliente_atualizado = None
    while True:
        evento_ed, valores_ed = janela_edicao.read()
        if evento_ed in (sg.WINDOW_CLOSED, 'Cancelar'):
            break
        if evento_ed == 'Salvar Alterações':
            cliente_atualizado = [
                valores_ed['-NOME-'],
                valores_ed['-CPF-'],
                valores_ed['-TELEFONE-'],
                valores_ed['-EMAIL-'],
                valores_ed['-ENDERECO-']
                # Adicionar valores para outros campos se existirem, ex: valores_ed['-DATA_NASCIMENTO-']
            ]
            break
    janela_edicao.close()
    return cliente_atualizado

# INTERFACE PRINCIPAL 
python_exe = sys.executable
cabecalho_tabela, dados_tabela_mestra = carregar_clientes()

layout = [
    [sg.Text('Gerenciamento de Clientes', font=('Helvetica', 18))],
    [sg.Text('Filtrar:'), sg.Input(key='-FILTRO-', enable_events=True)],
    [sg.Table(values=dados_tabela_mestra, headings=cabecalho_tabela, max_col_width=25,
              auto_size_columns=True, display_row_numbers=True, justification='left',
              num_rows=15, key='-TABELA_CLIENTES-', row_height=25)],
    [sg.Button('Cadastrar Novo Cliente'),
     sg.Button('Editar Selecionado', button_color=('white', 'green')),
     sg.Button('Deletar Selecionado', button_color=('white', 'red'))]
]

janela = sg.Window('Painel de Clientes', layout, resizable=True)
dados_exibidos_atualmente = dados_tabela_mestra

while True:
    evento, valores = janela.read()
    if evento == sg.WINDOW_CLOSED:
        break

    if evento == '-FILTRO-':
        termo_busca = valores['-FILTRO-'].lower()
        dados_filtrados = [
            cliente for cliente in dados_tabela_mestra
            if any(termo_busca in str(c).lower() for c in cliente)
        ] if termo_busca else dados_tabela_mestra
        janela['-TABELA_CLIENTES-'].update(values=dados_filtrados)
        dados_exibidos_atualmente = dados_filtrados

    if evento == 'Cadastrar Novo Cliente':
        subprocess.Popen([python_exe, 'gui_cadastro_cliente.py']) 
    if evento in ('Editar Selecionado', 'Deletar Selecionado'):
        if valores['-TABELA_CLIENTES-']:
            indice_na_tabela = valores['-TABELA_CLIENTES-'][0]
            
            dados_do_cliente_selecionado = dados_exibidos_atualmente[indice_na_tabela]
            
            # Precisamos encontrar o índice real desse cliente na lista mestra
            # para garantir que removemos ou editamos o cliente correto no arquivo CSV.
            try:
                indice_real_na_mestra = dados_tabela_mestra.index(dados_do_cliente_selecionado)
            except ValueError:
                
                sg.popup_error("Erro: Cliente selecionado não encontrado na base de dados principal.")
                continue 

            if evento == 'Editar Selecionado':
                dados_atualizados = criar_janela_edicao_cliente(dados_do_cliente_selecionado)
                if dados_atualizados:
                    dados_tabela_mestra[indice_real_na_mestra] = dados_atualizados
                    if salvar_clientes(cabecalho_tabela, dados_tabela_mestra):
                        
                        janela['-TABELA_CLIENTES-'].update(values=dados_tabela_mestra)
                        dados_exibidos_atualmente = dados_tabela_mestra 
                        sg.popup_ok("Cliente atualizado com sucesso!")
                    else:
                        sg.popup_error("Falha ao salvar as alterações do cliente.")

            elif evento == 'Deletar Selecionado':
                confirmar = sg.popup_yes_no(f"Tem certeza que deseja deletar o cliente {dados_do_cliente_selecionado[0]}?", title="Confirmar Exclusão")
                if confirmar == 'Yes':
                    del dados_tabela_mestra[indice_real_na_mestra]
                    if salvar_clientes(cabecalho_tabela, dados_tabela_mestra):
                        # Após a exclusão, recarregamos a tabela exibida
                        janela['-TABELA_CLIENTES-'].update(values=dados_tabela_mestra)
                        dados_exibidos_atualmente = dados_tabela_mestra # Atualiza a lista exibida também
                        sg.popup_ok("Cliente deletado com sucesso!")
                    else:
                        sg.popup_error("Falha ao deletar o cliente.")
        else:
            sg.popup_warning("Por favor, selecione um cliente na tabela para editar ou deletar.")

janela.close()