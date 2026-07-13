import requests
import sqlite3
import logging
import os
from config import API_URL
from dotenv import load_dotenv

load_dotenv()

class JokePipeline:
    
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        # Setup Loggin immdediately
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("pipeline.log"),
                logging.StreamHandler()
            ]
        )

        # Setup Database (Table Creation) once
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS jokes (setup TEXT, punchline TEXT)')
        conn.commit()
        conn.close()

    def fetch_joke(self):
        logging.info("Fetching a new joke ... ")
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status
        return response.json()
    
    def save_joke(self, joke_data):
        setup = joke_data.get("setup", "No setup")
        punchline = joke_data.get("punchline", "No punchline")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Check for the comming data
        cursor.execute('SELECT * FROM jokes WHERE setup = ?', (setup,))
        if cursor.fetchone():
            logging.info("Duplicate detected! Skipping.")
        else:
            # Insert
            cursor.execute('INSERT INTO jokes (setup, punchline) VALUES (?,?)', (setup, punchline))
            conn.commit()
            
            logging.info(f"Saving jokes to {self.db_name}")
        conn.close()

    def run(self):
        try:
          data = self.fetch_joke()
          self.save_joke(data)
          logging.info("Pipeline complete.")
        except Exception as e:
            logging.error(f"Pipeline failed: {e}")        

if __name__ == "__main__":
    pipeline = JokePipeline()
    pipeline.run()            
