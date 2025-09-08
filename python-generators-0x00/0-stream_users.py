#!/usr/bin/python3

# 0-stream_users.py

seed = __import__('seed')

connection = seed.connect_to_prodev()

if connection:
    user_generator = seed.stream_users(connection)
    print("Streaming users:")
    for user in user_generator:
        print(user)

    connection.close()