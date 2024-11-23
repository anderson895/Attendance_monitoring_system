# database.py
import mysql.connector
from mysql.connector import Error

class Database:
    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                database='gab_attendance',  
                user='root',             
                password='' 
            )
            if conn.is_connected():
                print("Database connection successful.")
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None
        
    def execute_query(self, query, params):
        # This method executes a query with the provided parameters and returns the result
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()  # Fetch all rows from the query result
            cursor.close()
            conn.close()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        
    # Modify the verify_login method to return both role and user_id
    def verify_login(self, username, password):
        query = "SELECT id, role FROM users WHERE username = %s AND password = %s"
        result = self.execute_query(query, (username, password))
        if result:
            user_id, role = result[0]  # Assuming result[0] contains the row (id, role)
            return user_id, role
        return None

# Create a global instance of the Database class
db_instance = Database()
