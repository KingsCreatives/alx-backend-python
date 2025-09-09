import sys
seed = __import__('seed')


def stream_user_ages():
   
    connection = None
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT age FROM user_data")
            
            for row in cursor:
                yield row[0]
                
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    finally:
        if connection:
            connection.close()


def calculate_average_age():
    
    total_age = 0
    count = 0
   
    for age in stream_user_ages():
        total_age += age
        count += 1
        
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found.")



if __name__ == "__main__":
    calculate_average_age()