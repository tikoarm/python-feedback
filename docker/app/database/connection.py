import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()
db_host = os.getenv("MYSQL_HOST")
db_port = int(os.getenv("MYSQL_PORT", 3306))
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_database = os.getenv("MYSQL_DATABASE")

if not db_host or not db_port or not db_user or not db_password or not db_database:
    raise ValueError("Missing DataBase credentials in environment variables.")


import time

def get_connection():
    for attempt in range(10):
        try:
            return mysql.connector.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_database,
            )
        except mysql.connector.Error as e:
            print(f"[DB] Connection attempt {attempt + 1} failed: {e}")
            time.sleep(3)
    raise Exception("⚠️ Failed to connect to the database after multiple attempts.")
