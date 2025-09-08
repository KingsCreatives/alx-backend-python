seed = __import__('seed')

connection = seed.connect_db()

if connection:
    print("Connection to MySQL server successful")
    seed.create_database(connection)
    connection.close()

    
    connection = seed.connect_to_prodev()
    if connection:
        print("Connected to ALX_prodev database")
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        
        print("\nFirst 5 rows from the user_data table:")
        for row in rows:
            print(row)
            
        cursor.close()
        connection.close()
        print("\nAll tasks completed and connections closed.")