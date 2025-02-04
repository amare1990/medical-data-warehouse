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

    def store_in_db(self, df, table_name="medical_data", default_id_value=100000):
        """Stores the cleaned data in a PostgreSQL database."""
        if df is None or df.empty:
            logging.error("No data to store in the database.")
            return

        # Ensure no null values in important columns, e.g., 'id'
        if 'id' in df.columns:
            # Fill NULL 'id' with a default value
            df['id'] = df['id'].fillna(default_id_value)  # Use passed argument
            # Option 2: Drop rows where 'id' is NULL
            # df = df.dropna(subset=['id'])  # Drop rows where 'id' is NULL

        # Fill or drop other important columns (if needed)
        if 'my_first_dbt_model_id' in df.columns:
            df['my_first_dbt_model_id'] = df['my_first_dbt_model_id'].fillna(default_id_value)  # Adjust as needed

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

            # Insert data using parameterized queries
            insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))});"
            for _, row in df.iterrows():
                cursor.execute(insert_query, tuple(row))

            conn.commit()
            cursor.close()
            conn.close()

            logging.info(f"Data stored in PostgreSQL database (Table: {table_name})")

        except Exception as e:
            logging.error(f"Error storing data in PostgreSQL: {e}")
