# telegram_scraper.py
import os
import logging
from telethon import TelegramClient
from dotenv import load_dotenv
from telethon.sessions import MemorySession
import nest_asyncio

# Apply nested asyncio for Jupyter Notebooks (if needed)
nest_asyncio.apply()

# Load environment variables
load_dotenv()

class TelegramScraper:
    def __init__(self, download_folder='downloads'):
        self.api_id = os.getenv('API_ID')
        self.api_hash = os.getenv('API_HASH')

        if not self.api_id or not self.api_hash:
            raise ValueError("API_ID and API_HASH must be set in the .env file!")

        self.client = TelegramClient(MemorySession(), self.api_id, self.api_hash)

        # Use Telegram channel usernames (not full URLs)
        self.channels = [
            'DoctorsET',
            'lobelia4cosmetics',
            'yetenaweg',
            'EAHCI'
        ]

        self.data = []  # List to store preprocessed data

        self.main_download_folder = download_folder
        os.makedirs(self.main_download_folder, exist_ok=True)  # Ensure folder exists

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
