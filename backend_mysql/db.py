import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST','127.0.0.1'),
        user=os.getenv('DB_USER','root'),
        password=os.getenv('DB_PASS',''),
        database=os.getenv('DB_NAME','library_db'),
        autocommit=True
    )
