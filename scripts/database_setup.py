import os
import psycopg2
import logging
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class DatabaseHandler:
    def __init__(self):
        """Initialize PostgreSQL connection using credentials from .env"""
        self.db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" \
                      f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        self.dbt_project_name = os.getenv("DBT_PROJECT_NAME", "my_project")

    def store_in_db(self, df, table_name="medical_data"):
        """Stores the cleaned data in a PostgreSQL database."""
        if df is None or df.empty:
            logging.error("No data to store in the database.")
            return

        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()

            # Create table if not exists
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                {", ".join([f"{col} TEXT" for col in df.columns])}
            );
            """
            cursor.execute(create_table_query)
            conn.commit()

            # Insert data
            for _, row in df.iterrows():
                values = "', '".join(str(value) for value in row)
                insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ('{values}');"
                cursor.execute(insert_query)

            conn.commit()
            cursor.close()
            conn.close()

            logging.info(f"Data stored in PostgreSQL database (Table: {table_name})")

        except Exception as e:
            logging.error(f"Error storing data in PostgreSQL: {e}")
