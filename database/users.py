from database.connection import get_connection


def add_user(name, email, phone=None):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO Users (name, email, phone)
            VALUES (?, ?, ?)
        """

        cursor.execute(query, (name, email, phone))
        connection.commit()

        print("User added successfully!")

    except Exception:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()