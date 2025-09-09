seed = __import__('seed')

connection = seed.connect_to_prodev()

def stream_users(connection):
    return seed.stream_data(connection, 'user_data')


if connection:
    user_generator = stream_users(connection)
    print("Streaming users:")
    for user in user_generator:
        print(user)

    connection.close()