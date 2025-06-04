# src/app.py
from flask import Flask, render_template,session
from config import config
from extension.extesion import db, mail, login_manager
from filtros import format_hora, format_fecha
from routes import register_blue
from entities.ModelUser import ModelUser

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['dev'])

    # Inicializar extensiones
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Filtros personalizados
    app.jinja_env.filters['format_hora'] = format_hora
    app.jinja_env.filters['format_fecha'] = format_fecha

    # Registrar Blueprints
    register_blue(app)

    # Error 404
    @app.errorhandler(404)
    def status_404(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(401)
    def status_401(error):
        return render_template('401.html'), 401

    # Cargar el usuario en sesión
    @login_manager.user_loader
    def load_user(id):
        return ModelUser.get_by_id(db, id)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
