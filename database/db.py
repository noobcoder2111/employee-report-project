import os
import psycopg2
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()


def get_connection():
    """
    Opens and returns a new connection to the PostgreSQL database.
    Credentials are read from environment variables (set via .env),
    so no password is ever hard-coded here.
    """
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return connection