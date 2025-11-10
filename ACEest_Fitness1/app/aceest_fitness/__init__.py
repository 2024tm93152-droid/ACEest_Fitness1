from flask import Flask
from .views import main_bp

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('aceest_fitness.config.Config')
    if config:
        app.config.update(config)

    # Register Blueprints (views)
    app.register_blueprint(main_bp)

    return app
