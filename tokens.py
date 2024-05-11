import requests
import base64
from modules import terminal
from datetime import datetime

class Tokens:
    refresh_token = None
    access_token = None
    id_token = None
    refresh_token_issued = None
    access_token_issued = None
    refresh_token_timeout = 7  # days
    access_token_timeout = 1800  # seconds

class TokenManager:
    @staticmethod
    def post_access_token_automated(grant_type, code, credentials):
        headers = {
            'Authorization': f'Basic {base64.b64encode(bytes(f"{credentials.app_key}:{credentials.app_secret}", "utf-8")).decode("utf-8")}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': grant_type,
            'code': code,
            'redirect_uri': credentials.callback_url
        } if grant_type == 'authorization_code' else {
            'grant_type': 'refresh_token',
            'refresh_token': code
        }
        response = requests.post('https://api.schwabapi.com/v1/oauth/token', headers=headers, data=data)
        if not response.ok:
            terminal.color_print.error(f"Error while requesting token: {response.text}")
            return None
        return response.json()

    @staticmethod
    def update_token_file(tokens, file_name="tokens.json"):
        token_data = {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "id_token": tokens.id_token,
            "access_token_issued": tokens.access_token_issued.isoformat(),
            "refresh_token_issued": tokens.refresh_token_issued.isoformat()
        }
        with open(file_name, 'w') as file:
            json.dump(token_data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_token_file(file_name="tokens.json"):
        try:
            with open(file_name, 'r') as file:
                token_data = json.load(file)
                Tokens.refresh_token = token_data.get("refresh_token")
                Tokens.access_token = token_data.get("access_token")
                Tokens.id_token = token_data.get("id_token")
                Tokens.refresh_token_issued = datetime.fromisoformat(token_data.get("refresh_token_issued"))
                Tokens.access_token_issued = datetime.fromisoformat(token_data.get("access_token_issued"))
        except FileNotFoundError:
            terminal.color_print.error("Token file not found. Please authenticate to generate new tokens.")
