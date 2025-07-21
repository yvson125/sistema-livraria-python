============================================================
MANUAL DE INSTRUÇÕES - SISTEMA DE GERENCIAMENTO DE LIVRARIA
============================================================

Autor: [Jose Yvson e Sanclair Clemente]
Data: 21 de julho de 2025
Versão: 1.0

------------------------------------------------------------
1. VISÃO GERAL DO PROJETO
------------------------------------------------------------

Este é um sistema de desktop para gerenciamento de uma livraria, desenvolvido 
inteiramente em Python com a biblioteca PySimpleGUI. O sistema permite o 
cadastro, metodo CRUD, gerenciamento de livros e clientes, registro de vendas com baixa 
automática de estoque e a geração de relatórios financeiros e de inventário.
O armazenamento de dados é feito localmente em arquivos CSV.

------------------------------------------------------------
2. REQUISITOS
------------------------------------------------------------

Para executar este programa, é necessário ter o Python 3.11 (ou superior) 
instalado no computador. 

IMPORTANTE: Durante a instalação do Python, a opção "Add python.exe to PATH" 
deve ter sido marcada.

------------------------------------------------------------
3. INSTALAÇÃO E CONFIGURAÇÃO (Feito apenas uma vez)
------------------------------------------------------------

Para preparar o sistema para o primeiro uso, siga os passos abaixo.

PASSO 3.1: Configurar a Permissão do Terminal (PowerShell)
   a. Clique no menu Iniciar do Windows.
   b. Digite "PowerShell".
   c. Clique com o botão direito em "Windows PowerShell" e selecione 
      "Executar como administrador".
   d. Na janela azul/preta que se abrir, digite o comando abaixo e pressione Enter:
      Set-ExecutionPolicy RemoteSigned
   e. Ele fará uma pergunta de confirmação. Digite a letra 'S' e pressione Enter.
   f. Pode fechar esta janela de administrador.

PASSO 3.2: Instalar as Dependências do Projeto
   a. Abra um terminal normal (CMD ou PowerShell) dentro da pasta do projeto.
      (Dica: na barra de endereço da pasta, digite 'cmd' e pressione Enter).
   b. Crie o ambiente virtual com o comando:
      python -m venv venv
   c. Ative o ambiente virtual com o comando:
      .\venv\Scripts\activate
   d. Com o ambiente ativo (o nome "(venv)" aparecerá no terminal), 
      instale as bibliotecas necessárias com o comando:
      pip install PySimpleGUI --extra-index-url https://PySimpleGUI.net/install

Após estes passos, o sistema está pronto para ser usado.

------------------------------------------------------------
4. COMO USAR O PROGRAMA
------------------------------------------------------------

Para iniciar o sistema a qualquer momento, basta dar um **duplo-clique** no arquivo:

   >> INICIAR_LIVRARIA.bat <<

Este lançador cuidará de ativar o ambiente e executar a aplicação.

------------------------------------------------------------
5. DADOS DE LOGIN
------------------------------------------------------------

Ao iniciar o programa, use as seguintes credenciais para acessar o sistema:

   - Usuário: admin
   - Senha:   admin123
