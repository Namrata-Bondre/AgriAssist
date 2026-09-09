# =====================================================
# Test User Data Layer
# Tests saving a user into the Users table.
# =====================================================

from users import save_user
from connection import connection


# Test user details
name = "Test User"
email = "testuser@example.com"
phone = "9999999999"


# Save the test user
save_user(name, email, phone)


# Get the newly created user ID
cursor = connection.cursor()

cursor.execute(
    "SELECT user_id FROM Users WHERE email = ?",
    email
)

user = cursor.fetchone()

cursor.close()


# Display the generated user ID
if user:
    print("✅ User Created Successfully")
    print("User ID:", user[0])