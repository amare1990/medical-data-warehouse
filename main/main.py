
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
from scripts.object_detection import YoloObjectDetection
from scripts.database_setup import DatabaseHandler





if __name__ == '__main__':

  # Ignore warnings
  import warnings
  warnings.simplefilter("ignore", category=FutureWarning)

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

  """
  Object detection using YOLO
  """
  detector = YoloObjectDetection()
  model = detector.load_model()

  # Run the the detection method to detect all objects
  img_path = 'data/images/'
  detection_results = detector.detect_objects(img_path)

  # Extract relevant information such as bounding box, confidence score, and class label.
  processed_data = detector.process_detection_results()

  # Store processed data into the postgres database
  db_handler = DatabaseHandler()
  detector.store_to_database(processed_data, db_handler)
