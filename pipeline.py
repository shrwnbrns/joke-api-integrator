import requests
import sqlite3
import logging
from config import API_URL


class JokePipeline:
    
    def __init__(self, db_name):
        self.db_name = db_name
        #logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.basicConfig(level=logging.INFO)

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
        cursor.execute('CREATE TABLE IF NOT EXISTS jokes (setup TEXT, punchline TEXT)')
        cursor.execute('INSERT INTO jokes (setup, punchline) VALUES (?,?)', (setup, punchline))
        conn.commit()
        conn.close()

        logging.info(f"Saving jokes to {self.db_name}")

    def run(self):
        try:
          data = self.fetch_joke()
          self.save_joke(data)
          logging.info("Pipeline complete.")
        except Exception as e:
            logging.error(f"Pipeline failed: {e}")        

if __name__ == "__main__":
    pipeline = JokePipeline("jokes.db")
    pipeline.run()            
