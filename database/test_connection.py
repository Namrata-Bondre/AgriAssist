# =====================================================
#  Test Database Connection
# =====================================================

from connection import connection


# Check whether connection was successful
if connection:
    print("✅ Database Connected Successfully")

    # Close the connection after testing
    connection.close()
    print("✅ Connection Closed")