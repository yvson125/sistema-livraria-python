
import PySimpleGUI as sg
import csv
import subprocess
import sys
import os

sg.theme('DarkGreen3')

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, procurando na mesma pasta do script/exe. """
   
    try:
       
        base_path = sys._MEIPASS
    except Exception:
        
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)


python_exe = sys.executable


layout = [
    
    [sg.Text('Sistema de Gerenciamento de Livraria', font=('Helvetica', 20), justification='center')],
    [sg.VPush()],
    [sg.Button('Gerenciar Livros', size=(25, 2), font=('Helvetica', 12))],
    [sg.Button('Gerenciar Clientes', size=(25, 2), font=('Helvetica', 12))],
    [sg.Button('Registrar Nova Venda', size=(25, 2), font=('Helvetica', 12), button_color=('white', 'green'))],
    [sg.Button('Ver Relatório de Estoque', size=(25, 2), font=('Helvetica', 12), button_color=('white', 'purple'))],
    [sg.VPush()],
    [sg.Button('Sair', size=(15, 1), font=('Helvetica', 10))]
]


window_layout = [[sg.VPush()],
                 [sg.Column(layout, element_justification='center')],
                 [sg.VPush()]]

janela = sg.Window('Menu Principal - Livraria Top', window_layout, size=(500, 400), finalize=True, resizable=True)


while True:
    evento, valores = janela.read()

    if evento == sg.WINDOW_CLOSED or evento == 'Sair':
        break
        
    scripts = {
        'Gerenciar Livros': 'gerenciar_livros.py',
        'Gerenciar Clientes': 'gerenciar_clientes.py',
        'Registrar Nova Venda': 'gui_registrar_venda.py',
        'Ver Relatório de Estoque': 'gui_relatorio_estoque.py'
    }
    
    if evento in scripts:
        script_para_executar = scripts[evento]
        try:
            #  usando o python_exe do venv
            subprocess.Popen([python_exe, script_para_executar])
        except FileNotFoundError:
            sg.popup_error(f'Erro: O arquivo "{script_para_executar}" não foi encontrado.')

janela.close()