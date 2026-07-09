"""
from config import API_URL
import requests

def run_pipeline():
    print(f"Connecting to: {API_URL}")

if __name__ == "__main__":
    run_pipeline()    

"""    
import requests
import sqlite3
from config import API_URL

def run_pipeline():
    # 1. EXTRACT
    print(f"Connecting to {API_URL}")
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status() # Check if the request was successful
    data = response.json()

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

    print("Success! Joke saved to database.")

if __name__ == "__main__":
    run_pipeline()    