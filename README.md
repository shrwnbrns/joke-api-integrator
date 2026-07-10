# Joke API Integrator

## What is this?
This project is a data pipeline that automatically fetches a random joke from an online API and saves it securely into a local database (SQLite).

## Why I built it
I wanted to build a resilient system that doesn't just "run," but handles failures gracefully. 
- It logs progress.
- It detects network errors if the internet is down.
- It detects database errors if the file is locked or missing.

## How to use it
1. Clone the repository.
2. Make sure you have the `requests` library installed (`pip install requests`).
3. Run the pipeline:
   `python pipeline.py`

## What I learned
- Managing versions using Git branches.
- Handling unexpected crashes with `try...except` blocks.
- Logging processes for better debugging.
