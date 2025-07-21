
import PySimpleGUI as sg
import csv
import os
import sys  


def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def salvar_cliente_csv(cliente):
    nome_arquivo = resource_path('clientes.csv') 
    arquivo_existe = os.path.isfile(nome_arquivo)
    
    try:
        with open(nome_arquivo, mode='a', newline='', encoding='utf-8') as arquivo_csv:
            campos = ['nome', 'cpf', 'telefone', 'email', 'endereco', 'data_nascimento']
            escritor = csv.DictWriter(arquivo_csv, fieldnames=campos)
            
            if not arquivo_existe or arquivo_csv.tell() == 0:
                escritor.writeheader()
            
            escritor.writerow(cliente)
        return True
    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")
        return False


layout = [
    [sg.Text('Nome Completo:'), sg.Input(key='nome')],
    [sg.Text('CPF:'), sg.Input(key='cpf')],
    [sg.Text('Telefone:'), sg.Input(key='telefone')],
    [sg.Text('E-mail:'), sg.Input(key='email')],
    [sg.Text('Endereço:'), sg.Input(key='endereco')],
    [sg.Text('Data de Nascimento:'), sg.Input(key='data_nascimento')],
    [sg.Button('Cadastrar Cliente', button_color=('white', 'blue'))],
    [sg.Text('', size=(50, 2), key='mensagem')]
]

janela = sg.Window('Cadastro de Clientes - Livraria', layout, element_justification='c')


while True:
    evento, valores = janela.read()

    if evento == sg.WINDOW_CLOSED:
        break

    if evento == 'Cadastrar Cliente':
        campos_obrigatorios = ['nome', 'cpf', 'telefone', 'email', 'endereco', 'data_nascimento']
        if any(not valores[campo] for campo in campos_obrigatorios):
            janela['mensagem'].update('Por favor, preencha todos os campos.', text_color='red')
            continue

        try:
            cliente = {
                "nome": valores['nome'],
                "cpf": valores['cpf'],
                "telefone": valores['telefone'],
                "email": valores['email'],
                "endereco": valores['endereco'],
                "data_nascimento": valores['data_nascimento'],
            }
            
            if salvar_cliente_csv(cliente):
                janela['mensagem'].update('Cliente salvo com sucesso!', text_color='green')
                for campo in campos_obrigatorios:
                    janela[campo].update('')
            else:
                 janela['mensagem'].update('Erro ao salvar o cliente no arquivo.', text_color='red')

        except Exception as e:
            janela['mensagem'].update(f'Ocorreu um erro inesperado: {e}', text_color='red')

janela.close()