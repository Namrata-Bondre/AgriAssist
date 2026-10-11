from database.connection import get_connection


def get_prediction_history(user_id):
    connection = None
    cursor = None

    try:
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
                status,
                [condition],
                severity,
                recommendation,
                created_at
            FROM Predictions
            WHERE user_id = ?
            ORDER BY created_at DESC
        """

        cursor.execute(query, (user_id,))
        history = cursor.fetchall()

        return history

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()