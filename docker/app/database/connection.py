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


def get_connection():
    return mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_database,
    )
