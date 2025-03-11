import os

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define esse diretório como local de trabalho
os.chdir(script_dir)

print("Agora o diretório é:", os.getcwd())