from flask import Flask
from netspectre.config import Config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="web/static", template_folder="web/templates")
    app.config.from_object(config_class)
    config_class.init_app(app)

    from netspectre.web.routes import web_bp
    app.register_blueprint(web_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
