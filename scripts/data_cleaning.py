import os
import logging
import pandas as pd

import re
import sqlite3


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

    def clean_data(self, df):
        """Performs data cleaning tasks: duplicates removal, handling missing values, and format standardization."""
        if df is None:
            logging.error("DataFrame is None, skipping cleaning.")
            return None

        try:
            # Removing duplicates
            df.drop_duplicates(inplace=True)

            # Handling missing values (filling with empty string or mean for numeric)
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col].fillna("", inplace=True)
                else:
                    df[col].fillna(df[col].mean(), inplace=True)

            # Remove emojis
            # emoji_pattern = re.compile(
            #     "["
            #     "\U0001F600-\U0001F64F"  # emoticons
            #     "\U0001F300-\U0001F5FF"  # symbols & pictographs
            #     "\U0001F680-\U0001F6FF"  # transport & map symbols
            #     "\U0001F700-\U0001F77F"  # alchemical symbols
            #     "\U0001F780-\U0001F7FF"  # geometric shapes extended
            #     "\U0001F800-\U0001F8FF"  # supplemental arrows-c
            #     "\U0001F900-\U0001F9FF"  # supplemental symbols & pictographs
            #     "\U0001FA00-\U0001FA6F"  # chess symbols
            #     "\U0001FA70-\U0001FAFF"  # symbols & pictographs extended-a
            #     "\U00002702-\U000027B0"  # dingbats
            #     "\U000024C2-\U0001F251"
            #     "]+",
            #     flags=re.UNICODE
            # )

            # emoji_pattern.sub(r'', df['message'])


            logging.info("Data cleaning completed successfully.")
            return df
        except Exception as e:
            logging.error(f"Error during data cleaning: {e}")
            return None

    def save_cleaned_data(self, df):
        """Saves the cleaned data to a CSV file."""
        if df is not None:
            df.to_csv(self.cleaned_data_path, index=False)
            logging.info(f"Cleaned data saved to {self.cleaned_data_path}")
        else:
            logging.error("No data to save.")

    def store_in_db(self, df, table_name="medical_data"):
        """Stores the cleaned data in an SQLite database."""
        if df is None:
            logging.error("No data to store in the database.")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            conn.close()
            logging.info(f"Data stored in database at {self.db_path} (Table: {table_name})")
        except Exception as e:
            logging.error(f"Error storing data in database: {e}")
