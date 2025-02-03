import os
import pandas as pd
import numpy as np
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
    def __init__(self, limit=100):
        """Initialize the scraper with a set message limit."""
        self.api_id = os.getenv('API_ID')
        self.api_hash = os.getenv('API_HASH')

        if not self.api_id or not self.api_hash:
            raise ValueError("API_ID and API_HASH must be set in the .env file!")

        self.client = TelegramClient(MemorySession(), self.api_id, self.api_hash)

        # Get absolute path of the "data" folder at the root of your repo
        self.base_data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

        # Define subdirectories inside the "data" folder
        self.download_folder = os.path.join(self.base_data_folder, "downloads")
        self.text_data_folder = os.path.join(self.base_data_folder, "scraped_data")
        self.image_folder = os.path.join(self.base_data_folder, "images")
        self.merged_file = os.path.join(self.base_data_folder, "scraped_data.csv")  # Fixed

        # Ensure folders exist
        os.makedirs(self.download_folder, exist_ok=True)
        os.makedirs(self.text_data_folder, exist_ok=True)
        os.makedirs(self.image_folder, exist_ok=True)

        # Channels to scrape (only specified ones)
        self.image_channels = {
            'Chemed_Telegram_Channel': 'Chemed',
            'lobelia4cosmetics': 'lobelia4cosmetics'
        }

        self.text_channels = [
            'DoctorsET',
            'yetenaweg',
            'EAHCI',
            'Chemed',
            'lobelia4cosmetics'
        ]

        self.data = []  # List to store text messages
        self.limit = limit  # Number of messages to fetch

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    async def fetch_messages(self, channel, is_image_channel=False):
        """Fetch messages from a Telegram channel, downloading images if applicable."""
        try:
            logging.info(f"Fetching messages from {channel} (Limit: {self.limit})...")
            messages = await self.client.get_messages(channel, limit=self.limit)

            for message in messages:
                if message.text and not is_image_channel:
                    self.data.append({"channel": channel, "message": message.text.strip()})
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
                return

            file_path = await message.download_media(self.image_folder)
            logging.info(f"Downloaded image to {file_path}")
        except Exception as e:
            logging.error(f"Error downloading image: {e}")

    def append_scraped_data(self):
        """Reads all scraped files, appends data, and stores in a structured format."""
        all_files = [f for f in os.listdir(self.text_data_folder) if f.endswith(".txt")]

        if not all_files:
            logging.warning("No scraped files found!")
            return None

        for file in all_files:
            channel_name = file.replace(".txt", "")  # Extract channel name
            file_path = os.path.join(self.text_data_folder, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    messages = f.readlines()

                # Append data in structured format
                for msg in messages:
                    self.data.append({"channel": channel_name, "message": msg.strip()})

                logging.info(f"Appended {len(messages)} messages from {channel_name}")

            except Exception as e:
                logging.error(f"Error reading {file_path}: {e}")

    def save_to_csv(self):
        """Saves the aggregated scraped data into a CSV file."""
        if not self.data:
            logging.warning("No data available to save!")
            return

        df = pd.DataFrame(self.data)
        df.to_csv(self.merged_file, index=False)
        logging.info(f"Saved {len(df)} messages to {self.merged_file}")

    def get_dataframe(self):
        """Returns the aggregated data as a Pandas DataFrame."""
        if not self.data:
            logging.warning("No data available!")
            return None

        return pd.DataFrame(self.data)

    def process_scraped_data(self):
        """Executes the full pipeline: appending data and saving it in CSV format."""
        self.append_scraped_data()
        self.save_to_csv()

    async def run(self):
        """Runs the scraper."""
        await self.scrape_all_channels()
