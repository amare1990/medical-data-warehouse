
import asyncio
import nest_asyncio

# Apply nested asyncio (for Jupyter Notebook use cases)
nest_asyncio.apply()

from scripts.telegram_scrapping import TelegramScraper


if __name__ == '__main__':

  """
  Telegram scrapping
  """
  scraper = TelegramScraper()
  scraper = TelegramScraper(limit=200)  # Adjust limit if needed

  asyncio.run(scraper.run())  # Scrape messages asynchronously
  scraper.process_scraped_data()  # Save data in CSV format
