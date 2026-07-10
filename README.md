Joke API Integrator 🤖
A robust, object-oriented data pipeline designed to fetch random jokes from an online API and store them securely in a local SQLite database, with built-in duplicate detection.

🚀 Features
Object-Oriented Design: Utilizes the JokePipeline class structure for modular, reusable, and clean code.

Database Integration: Automatically creates and manages a local SQLite database.

Deduplication Logic: Intelligent "gatekeeper" system that checks the database before saving to prevent duplicate entries.

Automated Logging: Tracks pipeline activity and errors in real-time, making it easy to monitor the "robot's" health.

Resilient Design: Includes error handling to ensure the pipeline gracefully handles network issues or API failures.

🛠️ How it Works
The application follows a simple, professional pipeline flow:

Initialization: Sets up the database and configures logging.

Fetch: Connects to the Joke API to retrieve fresh content.

Validate: Checks the local storage to ensure the joke isn't already present.

Save/Skip: Inserts the new joke or skips it if a duplicate is detected.

📋 Prerequisites
Python 3.x

Required libraries: requests
