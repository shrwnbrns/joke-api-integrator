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
        
        # Define the session here so 'self.session' exists
        self.session = requests.Session()

        # Set the headers on this specific instance
        self.session.headers.update({
            "User-Agent": "My-App/1.0",
            "Accept": "application/json"
        })

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
        # Retrieve the key securely from the environment
        api_key = os.getenv("JOKE_API_KEY")

        # Inject the key into the sessio headers
        self.session.headers.update({"X-API-Key": api_key})

        # Add it to the session headers so it's sent with every request
        self.session.headers.update({"X-API-Key": api_key})

        try:
            logging.info("Fetching a new joke ... ")
            response = self.session.get(API_URL, timeout=5)
            response.raise_for_status
            return response.json()
        except requests.exceptions.Timeout as e:
            logging.error(f"The API is too slow, moving on! {e}")    
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch joke: {e}")
            return None
    
    def save_joke(self, joke_data):

        # Check the data you are receiving
        logging.info(f"DEBUG: Raw data received: {joke_data}")

        setup = joke_data.get("setup")
        punchline = joke_data.get("punchline")

        if not setup or not punchline:
            logging.warning("Received incomplate joke data. Dropping record.")
            return 

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
            if data is None:
                logging.warning("Pipeline stopping: No data fetched.")
                return 
            
            self.save_joke(data)
            logging.info("Pipeline complete.")
        except Exception as e:
            logging.error(f"Pipeline failed: {e}")        

if __name__ == "__main__":
    pipeline = JokePipeline()
    pipeline.run()            
