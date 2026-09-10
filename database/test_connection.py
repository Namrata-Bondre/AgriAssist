from database.connection import get_connection


def test_connection():
    try:
        connection = get_connection()

        print("Database connected successfully!")

        connection.close()
        print("Connection closed successfully!")

    except Exception as e:
        print("Database connection failed!")
        print("Error:", e)


if __name__ == "__main__":
    test_connection()