import mysql.connector
import csv


def connect_db():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1704"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    if connection.is_connected():
        cursor = connection.cursor()
        try:
          cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
          print("Database ALX_prodev was created successfully")
        except mysql.connector.Error as err :
          print(f"Error creating database: {err}")
        finally:
           cursor.close()

def connect_to_prodev():
   try:
      connection = mysql.connector.connect(
         host = "localhost",
         user= "root",
         password = "1704",
         database = "ALX_prodev"
      )
      return connection
   except mysql.connector.Error as err:
      print(f"Error connecting to ALX_prodev: {err}")
      return None


def create_table(connection):
    if connection.is_connected():
        cursor = connection.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
        """
        try:
            cursor.execute(create_table_query)
            print("Table user_data created successfully")
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")
        finally:
            cursor.close()


import csv

def insert_data(connection, file_path):
    if connection.is_connected():
        cursor = connection.cursor()
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                
                next(reader)
                for row in reader:
                    user_id, name, email, age = row
                    
                    cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (user_id,))
                    if not cursor.fetchone():
                        
                        insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
                        cursor.execute(insert_query, (user_id, name, email, age))
                connection.commit()
                print("Data inserted successfully")
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")
        finally:
            cursor.close()


def stream_data(connection, table_name):
    if connection.is_connected():
        cursor = connection.cursor(buffered=True)
        try:
         
            cursor.execute(f"SELECT * FROM {table_name}")
            
            for row in cursor:
                yield row
        except mysql.connector.Error as err:
            print(f"Error streaming data: {err}")
        finally:
            cursor.close()

# Stream Users
def stream_users(connection):
    return stream_data(connection, 'user_data')