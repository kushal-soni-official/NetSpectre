import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-netspectre-secret-123')
    
    # NVD API (No default placeholder, user MUST set it as an env variable)
    NVD_API_KEY = os.environ.get('NVD_API_KEY')
    
    # Storage Paths
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    
    @staticmethod
    def init_app(app):
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
