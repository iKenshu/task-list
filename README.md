# Task List API

This is a Task List API built with FastAPI and PostgreSQL. The application allows users to manage their todo items, including creating, reading, updating, and deleting tasks and todo lists.

## Requirements

- Python 3.12
- Docker and Docker Compose

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:iKenshu/task-list.git
   cd task-list
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application locally:

   ```bash
   fastapi run src/main.py
   ```

5. Access the API documentation at `http://127.0.0.1:8000/docs`.
6. Run the tests using `pytest` inside a virtual environment:

   ```bash
   pytest
   ```

## Running with Docker

1. Build and start the containers:

   ```bash
   docker-compose up --build
   ```

   or

   ```bash
   docker compose build
   docker compose up
   ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.
