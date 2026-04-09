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
        # NVD API Status Message
        if Config.NVD_API_KEY:
            print(f"\n[+] NVD API: [CONFIRMED] (Key found: {Config.NVD_API_KEY[:4]}...{Config.NVD_API_KEY[-4:]})")
        else:
            print("\n[!] NVD API: [MISSING] (Vulnerability lookups will be slower due to rate limits)")
            print("[TIP] Set 'NVD_API_KEY' environment variable for 2x faster scans.\n")
