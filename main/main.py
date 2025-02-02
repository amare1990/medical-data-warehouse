
import asyncio
import nest_asyncio

# Apply nested asyncio (for Jupyter Notebook use cases)
nest_asyncio.apply()

from scripts.telegram_scrapper import TelegramScraper


if __name__ == '__main__':

  """
  Telegram scrapping
  """
  scraper = TelegramScraper()
  asyncio.run(scraper.run())
