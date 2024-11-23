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
        
    def verify_login(self, username, password):
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT role, password FROM users WHERE username=%s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                if result and password == result[1]:  # Plain-text password comparison
                    return result[0]  # Return role
                else:
                    return None
            finally:
                conn.close()
        return None

   

  
