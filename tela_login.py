
import PySimpleGUI as sg
import csv
import subprocess
import sys
import os

sg.theme('DarkGreen3')

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, procurando na mesma pasta do script/exe. """
    
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)


def verificar_login(usuario, senha):
    caminho_arquivo = resource_path('usuarios.csv') 
    try:
        with open(caminho_arquivo, mode='r', newline='', encoding='utf-8-sig') as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                if linha['usuario'].strip() == usuario and linha['senha'].strip() == senha:
                    return True
    except FileNotFoundError:
        sg.popup_error(f'Arquivo de usuários não encontrado em: {caminho_arquivo}')
        return False
    return False


layout = [[sg.Text('Usuário'), sg.Input(key='-USER-')], [sg.Text('Senha'), sg.Input(key='-PASS-', password_char='*')], [sg.Button('Login'), sg.Button('Sair')]]
janela = sg.Window('Login', layout)
while True:
    evento, valores = janela.read()
    if evento in (sg.WIN_CLOSED, 'Sair'): break
    if evento == 'Login':
        if verificar_login(valores['-USER-'], valores['-PASS-']):
            sg.popup('Login bem-sucedido!', auto_close=True, auto_close_duration=1)
            janela.hide()
            python_exe = sys.executable
            
            subprocess.Popen([python_exe, 'main.py'])
            break
        else:
            sg.popup_error('Usuário ou senha inválidos.')
janela.close()