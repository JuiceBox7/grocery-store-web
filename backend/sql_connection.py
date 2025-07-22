import datetime
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
__cnx = None
user = os.getenv("MYSQL_USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")


def get_sql_connection():
    print("Opening mysql connection")
    global __cnx

    if __cnx is None:
        __cnx = mysql.connector.connect(user=user, password=password, database=database)

    return __cnx
