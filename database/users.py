# =====================================================
# User Data Layer
# Handles saving users into the Users table.
# =====================================================

from connection import connection


# =====================================================
# Save User
# Saves one user's information into the database.
# =====================================================

def save_user(name, email, phone):
    """
    Saves a new user into the Users table.
    """

    # Create a cursor to execute SQL commands
    cursor = connection.cursor()

    # SQL query to insert user information
    query = """
        INSERT INTO Users
        (name, email, phone)
        VALUES (?, ?, ?)
    """

    # Execute query with user details
    cursor.execute(
        query,
        name,
        email,
        phone
    )

    # Save changes permanently in the database
    connection.commit()

    # Close the cursor
    cursor.close()

    print("✅ User Saved Successfully")