from flask import Flask
from flask_socketio import SocketIO
from backend.config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

socketio = SocketIO(cors_allowed_origins="*")

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="web/static", template_folder="web/templates")
    app.config.from_object(config_class)
    config_class.init_app(app)

    # Initialize extensions
    socketio.init_app(app, message_queue=app.config['CELERY_BROKER_URL'])

    # Register blueprints safely to avoid circular imports
    from backend.web.routes import web_bp
    app.register_blueprint(web_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
