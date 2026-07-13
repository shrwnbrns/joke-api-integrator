# Joke API Integrator

A robust, configuration-driven backend pipeline that fetches random jokes from an online API and persists them to a local SQLite database. 

This project is designed with production-ready standards, including environment variable management, structured logging, and defensive error handling.

## Features
* **Dynamic Configuration:** Uses `.env` files to manage settings, keeping sensitive configuration out of the source code.
* **Resilient Pipeline:** Implements `try...except` blocks and short-circuit logic to ensure the pipeline fails gracefully without crashing.
* **Professional Observability:** Maintains a `pipeline.log` file with timestamps and severity levels (INFO, WARNING, ERROR) to track execution history and debug issues.
* **Duplicate Prevention:** Checks the database before inserting to ensure unique entries.

## Getting Started

### Prerequisites
* Python 3.x
* `requests` and `python-dotenv` libraries

### Installation
1. Clone this repository:
   ```bash
   git clone [https://github.com/shrvnbrns/joke-api-integrator.git](https://github.com/shrvnbrns/joke-api-integrator.git)