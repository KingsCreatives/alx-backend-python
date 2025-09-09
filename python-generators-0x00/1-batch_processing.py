import sys

from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    connection = None
    try:
        connection = connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                yield rows
    except Exception as e:
        print(f"An error occurred in stream_users_in_batches: {e}", file=sys.stderr)
    finally:
        if connection:
            connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user