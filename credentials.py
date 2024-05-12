import os
from dotenv import load_dotenv
from modules import terminal
from config import DEBUG_MODE

class Credentials:
    app_key = None
    app_secret = None
    callback_url = None
    account_hash = None
    account_number = None

    @classmethod
    def load_credentials(cls):
        load_dotenv()
        cls.app_key = os.getenv('APP_KEY')
        cls.app_secret = os.getenv('APP_SECRET')
        cls.callback_url = os.getenv('CALLBACK_URL')
        if not cls.validate_credentials():
            if DEBUG_MODE:
                terminal.color_print.error("Failed to load or validate credentials.")
            quit()
        terminal.color_print.info("Credentials loaded and validated successfully.")

    @classmethod
    def validate_credentials(cls):
        if not cls.app_key or not cls.app_secret:
            terminal.color_print.error("No app key or app secret found. Please check your .env file.")
            return False
        if len(cls.app_key) != 32:
            terminal.color_print.error(f"Invalid app key length: {len(cls.app_key)}. Expected length is 32.")
            return False
        if len(cls.app_secret) != 16:
            terminal.color_print.error(f"Invalid app secret length: {len(cls.app_secret)}. Expected length is 16.")
            return False
        return True
