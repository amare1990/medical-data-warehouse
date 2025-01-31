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


    async def start_client(self):
        """Starts the Telegram client."""
        await self.client.start()
        logging.info("Telegram client started.")

    async def fetch_messages(self, channel):
        """Fetches messages from a given Telegram channel."""
        async with self.client:
            logging.info(f"Fetching messages from {channel}...")
            messages = await self.client.get_messages(channel, limit=100)
            for message in messages:
                if message.text:
                    self.data.append(message.text)
            logging.info(f"Fetched {len(messages)} messages from {channel}.")


    async def scrape_all_channels(self):
        """Scrapes all channels asynchronously."""
        await self.start_client()
        for channel in self.channels:
            await self.fetch_messages(channel)
        logging.info("Scraping completed.")

