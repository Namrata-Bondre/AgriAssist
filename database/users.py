from database.connection import get_connection

def add_user(name, email, phone=None):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Users (name, email, phone)
        VALUES (?, ?, ?)
    """

    cursor.execute(query, (name, email, phone))
    connection.commit()

    cursor.close()
    connection.close()

    print("User added successfully!")