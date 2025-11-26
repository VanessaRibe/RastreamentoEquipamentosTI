# create_admin.py (Refatorado para ser chamado pelo app.py)

from extensions import db
from models import User, Predio, Sala
from config import Config
import sys


def initialize_database():
    """Cria o Admin e Locais Iniciais. Chamado apenas se o DB estiver vazio."""

    # NOTA: O app_context já foi criado no app.py antes de chamar esta função.

    print("--- Inicializando Dados ---")

    # 1. Criação do Usuário Admin Padrão
    # OBS: O código de deleção forçada foi removido, pois o if User.query.count() == 0
    # no app.py já garante que esta função só rode na primeira vez.

    admin_user = User(username='admin', is_admin=True)
    admin_user.set_password('SUA_NOVA_SENHA_FORTE')  # <<<< USE A SENHA QUE VOCÊ DEFINIU!
    db.session.add(admin_user)

    # 2. Limpeza e Criação dos Locais (Recriação para garantir ID 1)
    # ATENÇÃO: As tabelas já foram criadas pelo db.create_all() no app.py
    # O código abaixo DEVE ser capaz de rodar sem User.query.count()

    # Limpamos apenas para o caso de ter sobrado lixo (embora o User.query.count()==0 já seja a checagem)
    # db.session.query(Sala).delete()
    # db.session.query(Predio).delete()
    # db.session.commit()

    print("Criando locais...")

    # 3. Criação dos Locais Iniciais
    locais_iniciais = [
        ('Sede Principal', 'Estoque TI Central'),
        ('Sede Principal', 'Sala 101 - TI'),
        ('Filial Norte', 'Estoque TI Filial'),
    ]

    predios_criados = {}
    for predio_nome, _ in locais_iniciais:
        if predio_nome not in predios_criados:
            predio = Predio(nome=predio_nome)
            db.session.add(predio)
            db.session.flush()
            predios_criados[predio_nome] = predio

    for predio_nome, sala_nome in locais_iniciais:
        predio = predios_criados[predio_nome]
        nova_sala = Sala(nome=sala_nome, predio=predio)
        db.session.add(nova_sala)

    db.session.commit()
    print("Sucesso: Locais iniciais criados.")

# O bloco if __name__ == '__main__': foi removido para evitar a execução duplicada.