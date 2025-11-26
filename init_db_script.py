# init_db_script.py

import os
from app import create_app
from extensions import db
from models import User
import subprocess

# 1. Cria a aplicação Flask
app = create_app()


def run_db_setup():
    with app.app_context():
        # Verifica se o DB está vazio (se não houver usuários, é a primeira execução)
        user_count = db.session.query(User).count()

        if user_count == 0:
            print("--- EXECUTANDO SETUP INICIAL DO DB ---")

            # Aqui chamamos o create_admin.py como um processo externo para garantir que tudo rode no contexto certo
            try:
                # Comando que executa o script create_admin.py (cria admin e locais)
                # Usamos python -c para rodar o script diretamente no ambiente
                subprocess.run(["python", "create_admin.py"], check=True, capture_output=True, text=True)
                print("--- SETUP INICIAL COMPLETO. O Admin foi criado. ---")
            except subprocess.CalledProcessError as e:
                print(f"ERRO CRÍTICO AO RODAR create_admin.py: {e.stdout} {e.stderr}")
                raise e  # Força a falha se a inicialização falhar


# 2. Executa a inicialização
run_db_setup()

# 3. Este script não retorna nada, apenas configura o DB