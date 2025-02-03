import os
import logging
import pandas as pd


class DataProcessor:
    def __init__(self, raw_data_path='../data/scraped_data.csv', cleaned_data_path='../data/cleaned_data.csv', db_path='../data/medical_data.db'):
        """
        Initializes the DataProcessor class.

        :param raw_data_path: Path to the raw data file.
        :param cleaned_data_path: Path to save the cleaned data.
        :param db_path: Path to SQLite database.
        """
        self.raw_data_path = raw_data_path
        self.cleaned_data_path = cleaned_data_path
        self.db_path = db_path

        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.cleaned_data_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_data(self):
        """Loads raw data from CSV into a Pandas DataFrame."""
        try:
            df = pd.read_csv(self.raw_data_path)
            logging.info(f"Successfully loaded raw data from {self.raw_data_path}")
            return df
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            return None
