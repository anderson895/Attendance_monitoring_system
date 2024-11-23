# database.py
import mysql.connector
from mysql.connector import Error

class Database:
    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                database='login_system',
                user='root',
                password=''  # Replace with your actual DB password
            )
            if conn.is_connected():
                print("Database connection successful.")
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

   

  
