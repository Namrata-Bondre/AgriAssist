from database.connection import get_connection

def get_prediction_history(user_id):
    connection = get_connection()
    cursor = connection.cursor()

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

    cursor.execute(query, (user_id,))

    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return history