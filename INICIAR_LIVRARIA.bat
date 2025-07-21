@echo off
echo Iniciando o Sistema da Livraria...

:: Garante que todos os comandos rodem a partir da pasta onde o .bat está
cd /d "%~dp0"

echo.
echo -- Usando o Python do Ambiente Virtual para executar a aplicacao --
echo.

:: Executa o tela_login.py usando o python.exe de dentro da pasta venv
:: Esta é a forma mais garantida de funcionar.
call "venv\Scripts\python.exe" tela_login.py

echo.
echo O programa foi fechado. Pressione qualquer tecla para sair.
pause