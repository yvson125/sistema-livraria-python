
import PySimpleGUI as sg
import csv
import os
import sys  # Adicionado


def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def salvar_livro_csv(livro):
    nome_arquivo = resource_path('livros.csv') # USA A FUNÇÃO
    arquivo_existe = os.path.isfile(nome_arquivo)
    try:
        with open(nome_arquivo, mode='a', newline='', encoding='utf-8') as f:
            campos = ['titulo', 'autor', 'categoria', 'quantidade', 'preco', 'isbn']
            escritor = csv.DictWriter(f, fieldnames=campos)
            if not arquivo_existe or f.tell() == 0:
                escritor.writeheader()
            escritor.writerow(livro)
        return True
    except IOError:
        return False


layout = [
    [sg.Text('Título:'), sg.Input(key='titulo')],
    [sg.Text('Autor:'), sg.Input(key='autor')],
    [sg.Text('Categoria:'), sg.Input(key='categoria')],
    [sg.Text('Quantidade:'), sg.Input(key='quantidade')],
    [sg.Text('Preço (R$):'), sg.Input(key='preco')],
    [sg.Text('ISBN:'), sg.Input(key='isbn')],
    [sg.Button('Cadastrar Livro', button_color=('white', 'green'))],
    [sg.Text('', size=(50, 2), key='mensagem')]
]

janela = sg.Window('Cadastro de Livros', layout, element_justification='c')


while True:
    evento, valores = janela.read()
    if evento == sg.WINDOW_CLOSED:
        break
    if evento == 'Cadastrar Livro':
        campos_obrigatorios = ['titulo', 'autor', 'categoria', 'quantidade', 'preco', 'isbn']
        if any(not valores[campo] for campo in campos_obrigatorios):
            janela['mensagem'].update('Por favor, preencha todos os campos.', text_color='red')
            continue
        try:
            quantidade_int = int(valores['quantidade'])
            preco_float = float(valores['preco'].replace(',', '.'))

            livro = {
                "titulo": valores['titulo'], "autor": valores['autor'],
                "categoria": valores['categoria'], "quantidade": quantidade_int,
                "preco": f"{preco_float:.2f}",
                "isbn": valores['isbn']
            }
            if salvar_livro_csv(livro):
                janela['mensagem'].update('Livro cadastrado com sucesso!', text_color='green')
                for campo in campos_obrigatorios:
                    janela[campo].update('')
            else:
                 janela['mensagem'].update('Erro ao salvar o livro no arquivo.', text_color='red')
        except ValueError:
            janela['mensagem'].update('Quantidade deve ser um número inteiro e Preço deve ser um número válido.', text_color='red')
        except Exception as e:
            janela['mensagem'].update(f'Ocorreu um erro inesperado: {e}', text_color='red')

janela.close()
