import requests
import sqlite3
import logging
from config import API_URL

# Setup logging to show the timestamp automatically
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    logging.info("Starting extraction process")
    
    try: 
        # 1. EXTRACT
        print(f"Connecting to {API_URL}")
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status() # Check if the request was successful
       
        data = response.json()
        logging.info("Data successfully extracted")

        # 2. TRANSFORM
        setup = data.get("setup", "No setup")
        punchline = data.get("punchline", "No punchline")
            
        # 3. LOAD"
        conn = sqlite3.connect('jokes.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS jokes (setup TEXT, punchline TEXT)')
        cursor.execute('INSERT INTO jokes (setup, punchline) VALUES (?,?)', (setup, punchline))
        conn.commit()
        conn.close()

        # 4. FINAL SUCCESS LOG
        print("Success! Joke saved to database.")

    except requets.exceptions.RequestException as e:    
        # If the API_URL is wrong, or the network is down
        logging.error(f"Failed to connect to {API_URL}: {e}")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:    
        # General safety net for unexpected errors
        logging.error(f"An unexpected error occured: {e}")

        

if __name__ == "__main__":
    run_pipeline()    