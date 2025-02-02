import os
import logging
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
from telethon.sessions import MemorySession
import nest_asyncio

# Apply nested asyncio (for Jupyter Notebook use cases)
nest_asyncio.apply()

# Load environment variables
load_dotenv()

class TelegramScraper:
    def __init__(self, download_folder='downloads', text_data_folder='scraped_data', image_folder='images'):
        self.api_id = os.getenv('API_ID')
        self.api_hash = os.getenv('API_HASH')

        if not self.api_id or not self.api_hash:
            raise ValueError("API_ID and API_HASH must be set in the .env file!")

        self.client = TelegramClient(MemorySession(), self.api_id, self.api_hash)

        # Channels to scrape images from
        self.image_channels = {
            'Chemed_Telegram_Channel': 'Chemed_Telegram_Channel',
            'lobelia4cosmetics': 'lobelia4cosmetics'
        }

        # All channels for text messages (optional)
        self.text_channels = [
            'DoctorsET',
            'yetenaweg',
            'EAHCI'
        ]

        self.data = []  # List to store text messages

        # Ensure folders exist
        self.download_folder = download_folder
        self.text_data_folder = text_data_folder
        self.image_folder = image_folder
        os.makedirs(self.download_folder, exist_ok=True)
        os.makedirs(self.text_data_folder, exist_ok=True)
        os.makedirs(self.image_folder, exist_ok=True)

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    async def fetch_messages(self, channel, is_image_channel=False):
        """Fetch messages from a Telegram channel, downloading images if applicable."""
        try:
            logging.info(f"Fetching messages from {channel}...")
            messages = await self.client.get_messages(channel, limit=100)

            for message in messages:
                if message.text and not is_image_channel:
                    self.data.append(message.text)
                    self.store_data(channel, message.text)

                if message.media and is_image_channel:
                    await self.download_image(message)

            logging.info(f"Fetched {len(messages)} messages from {channel}.")
        except Exception as e:
            logging.error(f"Error fetching messages from {channel}: {e}")

    async def scrape_all_channels(self):
        """Scrapes all text and image channels asynchronously."""
        await self.client.start()
        logging.info("Telegram client started.")

        # Create tasks for text-only channels
        text_tasks = [self.fetch_messages(channel) for channel in self.text_channels]

        # Create tasks for image-only channels
        image_tasks = [self.fetch_messages(channel, is_image_channel=True) for channel in self.image_channels.values()]

        # Run tasks concurrently
        await asyncio.gather(*text_tasks, *image_tasks)

        await self.client.disconnect()
        logging.info("Scraping completed and client disconnected.")

    def store_data(self, channel, data):
        """Stores text messages in a file per channel."""
        filename = os.path.join(self.text_data_folder, f"{channel}.txt")
        try:
            with open(filename, "a", encoding="utf-8") as file:
                file.write(data + "\n")
        except Exception as e:
            logging.error(f"Error writing to {filename}: {e}")

    async def download_image(self, message):
        """Downloads only image files from a message."""
        try:
            if message.file and message.file.ext not in ['.jpg', '.png', '.jpeg', '.gif', '.webp']:
                logging.info(f"Skipping non-image file: {message.file.name}")
                return  # Ignore non-image files (e.g., .mp4, .pdf)

            file_path = await message.download_media(self.image_folder)
            logging.info(f"Downloaded image to {file_path}")
        except Exception as e:
            logging.error(f"Error downloading image: {e}")

    async def run(self):
        """Runs the scraper."""
        await self.scrape_all_channels()
