import os
import requests
from dotenv import load_dotenv

load_dotenv()

class MetabaseService:
    def __init__(self):
        self.metabase_url = os.getenv('METABASE_URL', 'http://localhost:3000')
        self.metabase_user = os.getenv('METABASE_USER', 'admin@baseball.stats')
        self.metabase_password = os.getenv('METABASE_PASSWORD', 'admin123')
        self.session_token = None

    def get_session_token(self):
        """Get a session token from Metabase"""
        try:
            response = requests.post(
                f"{self.metabase_url}/api/session",
                json={
                    "username": self.metabase_user,
                    "password": self.metabase_password
                }
            )
            if response.status_code == 200:
                self.session_token = response.json().get('id')
                return True
        except Exception as e:
            print(f"Failed to get session token: {e}")
        return False

    def create_braves_dashboard(self):
        """Create a simplified dashboard for Braves stats"""
        if not self.session_token and not self.get_session_token():
            return None
            
        headers = {"X-Metabase-Session": self.session_token}
        
        try:
            # Create dashboard
            dashboard_response = requests.post(
                f"{self.metabase_url}/api/dashboard",
                headers=headers,
                json={
                    "name": "Atlanta Braves 2025 Statistics",
                    "description": "Team and player statistics for the 2025 Atlanta Braves"
                }
            )
            
            if dashboard_response.status_code == 200:
                return dashboard_response.json().get('id')
            
        except Exception as e:
            print(f"Failed to create dashboard: {e}")
        
        return None