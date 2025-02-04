
import asyncio
import nest_asyncio

# Apply nested asyncio (for Jupyter Notebook use cases)
nest_asyncio.apply()

import sys
import os

# Get the root directory of the project
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add it to sys.path
sys.path.append(ROOT_DIR)

print(f"Current working directory: {os.getcwd()}")
from scripts.telegram_scrapping import TelegramScraper
from scripts.data_cleaning import DataProcessor


if __name__ == '__main__':

  """
  Telegram scrapping
  """
  scraper = TelegramScraper()
  scraper = TelegramScraper(limit=200)  # Adjust limit if needed

  asyncio.run(scraper.run())  # Scrape messages asynchronously
  scraper.process_scraped_data()  # Save data in CSV format


  """
  Data cleaning and transformation
  """
  processor = DataProcessor()
  processor.process_data()
