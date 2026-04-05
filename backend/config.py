import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-netspectre-secret-123')
    
    # Celery & Redis settings
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # NVD API
    NVD_API_KEY = os.environ.get('NVD_API_KEY', '') # Optional, but recommended to avoid severe rate limiting
    
    # Storage Paths
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    
    @staticmethod
    def init_app(app):
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
