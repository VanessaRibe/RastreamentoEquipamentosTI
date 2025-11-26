# app.py (Versão FINAL com Setup de Emergência)

import os
from flask import Flask
from flask_login import current_user
from config import Config
from extensions import db, login_manager
from models import Notificacao, User
# Importar a função de inicialização (que está em create_admin.py)
from create_admin import initialize_database
from routes import main as main_blueprint


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Inicializa Extensões
    db.init_app(app)
    login_manager.init_app(app)

    # 2. Configura o User Loader
    @login_manager.user_loader
    def load_user(user_id):
        with app.app_context():
            return User.query.get(int(user_id))

    # 3. CRIAÇÃO E VERIFICAÇÃO DO DB NO CONTEXTO (SOLUÇÃO DE EMERGÊNCIA)
    with app.app_context():
        # Cria as tabelas se não existirem
        db.create_all()

        # Se não houver usuários (primeira execução), inicializa os dados
        if User.query.count() == 0:
            print("=== EXECUTANDO SETUP INICIAL DE DADOS (RENDER FREE TIER) ===")
            # Chama a função de inicialização que cria o Admin e Locais
            # A lógica completa está agora aqui, mas isolada.
            initialize_database()
            print("=== SETUP INICIAL COMPLETO. O Admin foi criado. ===")

    # 4. Cria a pasta para os QR Codes
    os.makedirs(app.config['QR_CODE_FOLDER'], exist_ok=True)

    # 5. Registro dos Blueprints
    app.register_blueprint(main_blueprint)

    # 6. Context Processor para Notificações
    @app.context_processor
    def inject_notifications_count():
        if current_user.is_authenticated:
            with app.app_context():
                count = Notificacao.query.filter_by(
                    usuario_alvo_id=current_user.id, lida=False
                ).count()
            return dict(notificacoes_nao_lidas_count=count)
        return dict(notificacoes_nao_lidas_count=0)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)