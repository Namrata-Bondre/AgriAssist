# =====================================================
# Prediction History Data Layer
# Fetches prediction history from the database.
# =====================================================

from connection import connection


# =====================================================
# Get Prediction History
# Returns all predictions made by a particular user.
# =====================================================

def get_prediction_history(user_id):
    """
    Fetches prediction history for a specific user.
    """

    # Create a cursor to execute SQL commands
    cursor = connection.cursor()

    # SQL query to fetch prediction history
    query = """
        SELECT
            prediction_id,
            user_id,
            image_path,
            crop,
            disease,
            confidence,
            created_at
        FROM Predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
    """

    # Execute query using the given user ID
    cursor.execute(query, user_id)

    # Fetch all prediction records
    predictions = cursor.fetchall()

    # Close the cursor after fetching data
    cursor.close()

    # Return prediction history
    return predictions