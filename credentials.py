
import os
from dotenv import load_dotenv
from modules import terminal

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
        cls.validate_credentials()

    @classmethod
    def validate_credentials(cls):
        if not cls.app_key or not cls.app_secret:
            terminal.color_print.error("No app key or app secret found. Please check your .env file.")
            quit()
        if len(cls.app_key) != 32 or len(cls.app_secret) != 16:
            terminal.color_print.error("Invalid app key or app secret. Please check your credentials.")
            quit()

        terminal.color_print.info("Credentials loaded successfully.")
